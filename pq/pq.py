import re
import json
from json.decoder import JSONDecodeError
from collections import OrderedDict
from lxml import etree

from parsel import Selector
from dicttoxml import dicttoxml

RE_CLEAN = re.compile('\s{2,}')
RE_HAS_TEXT = re.compile('text\(\)$|::text$')
RE_IS_HTML = re.compile('<.+?>')


def clean_text(text):
    """clean text for repetitive spaces"""
    text = text.strip()
    text = RE_CLEAN.sub(' ', text)
    return text


def is_xml(text):
    """check whether text stirng is xml or html code"""
    return bool(RE_IS_HTML.match(text.strip()))


class PQ:
    """Json or xml processor for xpath or css selector queries"""

    def __init__(self, data, to_text=False, to_text_all=False):
        """
        :param data: input data_xml, either xml or json content
        """
        self.data = data
        self.sel = self._make_selector(self.data)
        self.to_text = to_text
        self.to_text_all = to_text_all

    def _make_selector(self, data):
        """
        Creates a parsel Selector from data.
        Decides whether the data is json or xml, converts json to xml.
        :return: parsel.Selector
        """
        try:  # try to convert json -> xml, if not xml
            data = json.loads(data, object_pairs_hook=OrderedDict)
            text = dicttoxml(data).decode('utf-8')
        except (TypeError, JSONDecodeError):
            text = data
        return Selector(text=text)

    def _path(self, func_name, path, to_text=None, to_text_all=None, first=False):
        """Base function for self.xpath and self.css"""
        func = getattr(self.sel, func_name)
        path = self.process_path(path,
                                 func_name=func_name,
                                 to_text=to_text,
                                 to_text_all=to_text_all)
        if first:
            return func(path).extract_first()
        return func(path).extract()

    def xpath(self, path, to_text=None, to_text_all=None, first=False):
        """
        Selects html node from path.
        :param path: xpath
        :param first: only first result
        :param to_text: shortcut: adds '/text()' to path
        :param to_text_all: shortcut: adds '//text()' to path
        :return: List of nodes or a string
        """
        return self._path('xpath', path, to_text, to_text_all, first)

    def css(self, path, to_text=None, to_text_all=None, first=False):
        """
        Selects html node from path.
        :param path: css selector path
        :param first: only first result
        :param to_text: shortcut: adds '::text' to path
        :param to_text_all: shortcut: adds ' ::text()' to path
        :return: List of nodes or a string
        """
        return self._path('css', path, to_text, to_text_all, first)

    def process_path(self, path, func_name=None, to_text=None, to_text_all=None):
        """
        process xpath or css selector path.
        :param path: xpath or css selector path
        :param func_name: 'css'|'xpath'
        :param to_text: retrieve node's text rather than xml code
        :param to_text_all: retrieve node's all text rather than xml code
        :return: processed path
        """
        to_text = self.to_text if to_text is None else to_text
        to_text_all = self.to_text_all if to_text_all is None else to_text_all

        css = func_name == 'css'
        addon = ''
        if css:
            if to_text or to_text_all:
                addon = '::text' if to_text else ' ::text'
        else:
            if to_text or to_text_all:
                addon = '/text()' if to_text else '//text()'

        # xpath can have multiple paths
        paths = path.split('|') if not css else [path]
        # check if paths already have xpath
        paths = [p for p in paths if not RE_HAS_TEXT.findall(path)]
        path = '|'.join(p + addon for p in paths) if paths else path
        return path

    def output(self, results, compact=False, to_json=False, to_text=None, to_text_all=None):
        """
        outputs results to stdout
        :param results: list of result
        :param compact: compact output
        :param to_json: output as json
        :param to_text: output as text [defaults to self.to_text]
        :param to_text_all: output as all text (that is under node) [defaults to self.to_text_all]
        :return: result string
        """
        def result_to_json(r):
            # todo rework, only works for nodes with text
            # for example it will fail for <a> or <img> nodes if they have no text
            sel = Selector(text=r)
            name = sel.xpath('name(//*[text()])').extract_first()
            value = ''.join(sel.xpath('//text()').extract()).strip()
            return {name: value}
        # defaults
        to_text = self.to_text if to_text is None else to_text
        to_text_all = self.to_text_all if to_text_all is None else to_text_all
        if not isinstance(results, list):
            results = [results]

        if to_text_all:
            return clean_text(''.join(results))
        elif to_text or not is_xml(''.join(results)):
            return clean_text('\n'.join(results))
        elif to_json:
            result = json.dumps([result_to_json(r) for r in results], indent=2 if not compact else 0,)
            return result
        results = Selector(text=''.join(results))
        if compact:
            return results
        else:
            return etree.tostring(results.root, pretty_print=True)


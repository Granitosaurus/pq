import re
import json
from json.decoder import JSONDecodeError
from collections import OrderedDict

from parsel import Selector
from dicttoxml import dicttoxml


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

    @staticmethod
    def process_results(results, first_available=False):
        """
        process list of results.
        :param results: list of nodes or strings
        :param first_available: only take first value
        :return: processed results
        """
        if first_available:
            r = [r for r in results]
            return r[0] if r else None
        return results

    def process_path(self, path, func_name=None, to_text=None, to_text_all=None):
        """
        process xpath or css selector path.
        :param path: xpath or css selector path
        :param func_name: 'css'|'xpath'
        :param to_text: retrieve node's text rather than xml code
        :param to_text_all: retrieve node's all text rather than xml code
        :return: processed path
        """
        if to_text is None:
            to_text = self.to_text
        if to_text_all is None:
            to_text_all = self.to_text_all
        if re.findall('text\(\)|::text', path):
            # already has text
            return path
        css = func_name == 'css'
        addon = ''
        if css:
            if to_text or to_text_all:
                addon = '::text' if to_text else ' ::text'
        else:
            if to_text or to_text_all:
                addon = '/text()' if to_text else '//text()'
        paths = path.split('|') if not css else [path]
        path = '|'.join(p + addon for p in paths)
        return path

    @staticmethod
    def output(results, compact=False):
        """
        outputs results to stdout
        :param compact: compact output
        :param results: list of results
        :return: None
        """
        if compact:
            result = json.dumps(results)
        else:
            result = json.dumps(results, indent=4)
        print(result.replace('\\"', '"'))

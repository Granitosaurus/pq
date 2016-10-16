import re
import json
from json.decoder import JSONDecodeError
from collections import OrderedDict

from parsel import Selector
from dicttoxml import dicttoxml


class PQ:
    """Json or xml processor for xpath or css selector queries"""

    def __init__(self, data):
        """
        :param data: input data_xml, either xml or json content
        """
        self.data = data
        self.sel = self._make_selector(self.data)

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

    def _path(self, func_name, path, to_text=False, to_text_all=False, first=False):
        """Base function for self.xpath and self.css"""
        func = getattr(self.sel, func_name)
        path = self.process_path(path,
                                 func_name=func_name,
                                 to_text=to_text,
                                 to_text_all=to_text_all)
        if first:
            return func(path).extract_first()
        return func(path).extract()

    def xpath(self, path, to_text=False, to_text_all=False, first=False):
        """
        Selects html node from path.
        :param path: xpath
        :param first: only first result
        :param to_text: shortcut: adds '/text()' to path
        :param to_text_all: shortcut: adds '//text()' to path
        :return: List of nodes or a string
        """
        return self._path('xpath', path, to_text, to_text_all, first)

    def css(self, path, to_text=False, to_text_all=False, first=False):
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

    @staticmethod
    def process_path(path, func_name=None, to_text=False, to_text_all=False):
        """
        process xpath or css selector path.
        :param path: xpath or css selector path
        :param func_name: 'css'|'xpath'
        :param to_text: retrieve node's text rather than xml code
        :param to_text_all: retrieve node's all text rather than xml code
        :return: processed path
        """
        if re.findall('text\(\)|::text', path):
            # already has text
            return path
        css = func_name == 'css'
        if to_text:
            if not css:
                path += '/text()'
            else:
                path += '::text'
        elif to_text_all:
            if not css:
                path += '//text()'
            else:
                path += ' ::text'
        return path

    @staticmethod
    def output(results):
        """
        outputs results to stdout
        :param results: list of results
        :return: None
        """
        print(json.dumps(results, indent=4))

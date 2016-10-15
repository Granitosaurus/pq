from pq import PQ


class TestClass:

    # noinspection PyAttributeOutsideInit
    def setup_method(self):
        self.data_xml = """
        <root>
          <foo>bar
            <foo2>bar_inside</foo2>
          </foo>
          <gar>fir</gar>
        </root>
        """
        self.data_xml = self.data_xml.replace('\n', '').replace(' ', '')
        self.pq = PQ(self.data_xml)
        self.data_json = """
        {
          "root": [
            {
              "foo": "bar",
              "deep": {"foo2": "bar_inside"}
            },
            {
              "gar": "fir"
            }
          ]
        }
        """

    def test_selector_from_json(self):
        pq = PQ(self.data_json)
        self._test_selector(pq)

    def test_selector_from_xml(self):
        pq = PQ(self.data_xml)
        # self._test_selector(pq)

    def _test_selector(self, pq):
        # print(pq.sel.extract())
        print(pq.sel.xpath("//foo").extract())
        assert pq.xpath('//foo/text()') == ['bar']
        assert pq.css('foo::text') == ['bar']
        assert pq.xpath('//foo/text()', first=True) == 'bar'
        assert pq.css('foo::text', first=True) == 'bar'
        assert pq.xpath('//foo', first=True, to_text=True) == 'bar'
        assert pq.css('foo', first=True, to_text=True) == 'bar'
        assert pq.xpath('//foo2/text()') == ['bar_inside']
        assert pq.css('foo2::text') == ['bar_inside']

    def test_process_xpath(self):
        assert 'text()' not in self.pq.process_path('//foo', func_name='xpath')
        assert 'text()' in self.pq.process_path('//foo', func_name='xpath', to_text=True)
        assert '//text()' in self.pq.process_path('//foo', func_name='xpath', to_text_all=True)

    def test_process_css_path(self):
        assert '::text' not in self.pq.process_path('//foo', func_name='css')
        assert '::text' in self.pq.process_path('//foo', func_name='css', to_text=True)
        assert ' ::text' in self.pq.process_path('//foo', func_name='css', to_text_all=True)


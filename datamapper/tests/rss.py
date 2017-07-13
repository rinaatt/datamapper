import os.path as op
import unittest
from types import GeneratorType
from datamapper.spiders import YandexRssFeedSpider
from scrapy.http.response.xml import XmlResponse
from scrapy.selector import Selector
from scrapy.utils.misc import arg_to_iter

TESTS_DIR = op.abspath(op.dirname(__file__))


class TestYandexRssFeedSpider(unittest.TestCase):
    rss_file = op.join(TESTS_DIR, 'data', 'yandex_news.rss')

    def setUp(self):
        with open(self.rss_file, 'rb') as fp:
            self.response = XmlResponse(
                url='file:///'+self.rss_file.replace('\\', '/'),
                body=fp.read()
            )
        self.spider = YandexRssFeedSpider()

    def test_itertag(self):
        self.assertEqual(self.spider.itertag, 'item')

    def test_parse_items(self):
        items = self.spider.parse(self.response)
        self.assertTrue(isinstance(items, GeneratorType),
                        'must be generator')
        self.assertEqual(len(list(items)), 10)

    def test_namespaces(self):
        selector = Selector(self.response, type='xml')
        self.spider._register_namespaces(selector)
        self.assertGreaterEqual(len(selector.namespaces), 8,
                                'The namespaces must be equal '
                                'or greater of 8')

    def test_parse_node(self):
        selector = Selector(self.response, type='xml')
        self.spider._register_namespaces(selector)
        nodes = selector.xpath('//%s' % self.spider.itertag)
        ret = self.spider.parse_node(self.response, nodes[0])
        self.assertTrue(isinstance(ret, dict))
        ret_keys = list(ret.keys())
        ret_keys.sort()
        original_keys = ['title', 'link', 'guid',
                         'pub_date', 'description']
        original_keys.sort()
        self.assertSequenceEqual(ret_keys, original_keys)
        self.assertEqual(ret['pub_date'], '12 Jul 2017 06:13:46 +0300')
        self.assertEqual(ret['link'], 'https://news.yandex.ru/yandsearch'
                                      '?cl4url=ria.ru%2Fsyria%2F20170712%2'
                                      'F1498323462.html')


if __name__ == '__main__':
    unittest.main()

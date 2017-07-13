from scrapy.spiders import XMLFeedSpider
from scrapy.http.response.text import TextResponse
from parsel.selector import Selector


class RssFeedBaseSpider(XMLFeedSpider):
    name = 'rss_feed'
    iterator = 'xml'
    itertag = 'item'
    namespaces = [
        ('dc', 'http://purl.org/dc/elements/1.1/'),
        ('content', 'http://purl.org/rss/1.0/modules/content/'),
        ('atom', 'http://www.w3.org/2005/Atom'),
        ('thespringbox', 'http://www.thespringbox.com/dtds/'
                         'thespringbox-1.0.dtd'),
        ('media', 'http://search.yahoo.com/mrss/'),
        ('feedburner', 'http://rssnamespace.org/feedburner/ext/1.0'),
    ]
    custom_settings = {
        'ROBOTSTXT_OBEY': False
    }

    def parse_node(self, response: TextResponse, selector: Selector):
        return {
            'title': selector.xpath('title/text()').get(),
            'link': selector.xpath('link/text()').get(),
            'guid': selector.xpath('guid/text()').get(),
            'pub_date': selector.xpath('pubDate/text()').get(),
            'description': selector.xpath('description/text()').get(),
        }


class YandexRssFeedSpider(RssFeedBaseSpider):
    name = 'rss_feed_yandex'
    start_urls = ['https://news.yandex.ru/index.rss', ]

    def parse(self, response: TextResponse):
        """
        This function parses a sample response. Some contracts are mingled
        with this docstring.
        @url https://news.yandex.ru/index.rss
        @returns items 15 15
        @returns requests 0 0
        @scrapes title link guid pub_date description
        """
        return super().parse(response)

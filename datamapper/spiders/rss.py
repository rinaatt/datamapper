from scrapy.spiders import XMLFeedSpider
from .__mixins import ConfigureMixin


class RssFeedSpider(XMLFeedSpider, ConfigureMixin):
    iterator = 'xml'
    itertag = 'item'
    namespaces = [
        ('dc', 'http://purl.org/dc/elements/1.1/'),
        ('content', 'http://purl.org/rss/1.0/modules/content/'),
        ('atom', 'http://www.w3.org/2005/Atom'),
        ('thespringbox', 'http://www.thespringbox.com/dtds/thespringbox-1.0.dtd'),
        ('media', 'http://search.yahoo.com/mrss/'),
        ('feedburner', 'http://rssnamespace.org/feedburner/ext/1.0'),
    ]

    def parse_node(self, response, selector):
        pass

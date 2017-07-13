import six
from scrapy.crawler import CrawlerProcess, Crawler


class CustomCrawlerProcess(CrawlerProcess):

    def create_crawler(self, crawler_or_spidercls):
        """
        Return a :class:`~scrapy.crawler.Crawler` object.

        * If `crawler_or_spidercls` is a Crawler, it is returned as-is.
        * If `crawler_or_spidercls` is a Spider subclass, a new Crawler
          is constructed for it.
        * If `crawler_or_spidercls` is a string, this function finds
          a spider with this name in a Scrapy project (using spider loader),
          then creates a Crawler instance for it.
        """
        if isinstance(crawler_or_spidercls, Crawler):
            return crawler_or_spidercls
        return self._create_crawler(crawler_or_spidercls)

    def _create_crawler(self, spidercls):
        if isinstance(spidercls, six.string_types):
            spidercls = self.spider_loader.load(spidercls)
        return Crawler(spidercls, self.settings)


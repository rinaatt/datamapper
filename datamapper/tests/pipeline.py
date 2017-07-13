import os
import json
import unittest
import pytz
from datetime import datetime
from dateutil.parser import parse
from datamapper.settings import SQLITE_DB_PLACE
from datamapper.pipelines import RssFeedPipeline
from datamapper.models import RssNews, create_db_tables
from datamapper.spiders import RssFeedSpider


class TestRssFeedPipeline(unittest.TestCase):
    db_place = SQLITE_DB_PLACE
    items_data_file = 'data/rssfeed_items.json'

    def setUp(self):
        """
        Setup a temporary database
        """
        self.database = create_db_tables()
        self.spider = RssFeedSpider()
        with open(self.items_data_file, 'rb') as f:
            self.items = json.load(f, encoding='utf-8')

    def tearDown(self):
        self.database.close()
        os.remove(self.db_place)

    def test_process_one(self):
        item = self.items[0]
        pipeline = RssFeedPipeline(database=self.database)
        pipeline.process_item(item, self.spider)
        count = RssNews.select().count()
        news_piece = RssNews.select().first()
        self.assertEqual(count, 1)
        self.assertEqual(news_piece.title, item['title'])
        self.assertEqual(news_piece.link, item['link'])
        self.assertEqual(news_piece.guid, item['guid'])
        self.assertNotEqual(news_piece.pub_date, item['pub_date'])
        pub_date = parse(item['pub_date']).astimezone(tz=pytz.UTC)
        self.assertEqual(news_piece.pub_date, pub_date.isoformat(sep=' '))
        self.assertEqual(news_piece.description, item['description'])

    def test_process_serial(self):
        pipeline = RssFeedPipeline(database=self.database)
        for item in self.items:
            pipeline.process_item(item, self.spider)
        count = RssNews.select().count()
        self.assertEqual(count, len(self.items))


if __name__ == '__main__':
    unittest.main()

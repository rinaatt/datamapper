import os
import os.path as op
import json
import unittest
import pytz
from dateutil.parser import parse
from datamapper.pipelines import RssFeedPipeline
from datamapper.models import RssNews
from datamapper.spiders import RssFeedBaseSpider

TESTS_DIR = op.abspath(op.dirname(__file__))


def get_database():
    from datamapper.models import database, create_db_tables
    database.init(':memory:')
    create_db_tables(database)
    return database


class TestRssFeedPipeline(unittest.TestCase):
    items_data_file = op.join(TESTS_DIR, 'data', 'rssfeed_items.json')

    def setUp(self):
        """
        Setup a temporary database
        """

        self.db = get_database()
        self.spider = RssFeedBaseSpider()
        with open(self.items_data_file, 'rb') as f:
            self.items = json.load(f, encoding='utf-8')

    def tearDown(self):
        if not self.db.is_closed():
            self.db.close()

    def test_process_one(self):
        item = self.items[0]
        pipeline = RssFeedPipeline(db=self.db)
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
        pipeline = RssFeedPipeline(db=self.db)
        for item in self.items:
            pipeline.process_item(item, self.spider)
        count = RssNews.select().count()
        self.assertEqual(count, len(self.items))


if __name__ == '__main__':
    unittest.main()

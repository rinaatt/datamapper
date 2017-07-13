from pytz import UTC
from logging import ERROR
from dateutil.parser import parse as parse_date
from peewee import DatabaseError
from scrapy import Spider
from .spiders import RssFeedBaseSpider
from .models import create_db_tables, RssNews


class SQLiteBasePipeline:
    conn = None

    def __init__(self, database=None):
        if database is None:
            database = create_db_tables()
        self.db = database

    def open_spider(self, spider: Spider):
        self.db.connect()

    def close_spider(self, spider: Spider):
        self.db.close()


class RssFeedPipeline(SQLiteBasePipeline):

    def process_item(self, item: dict, spider: Spider):
        if isinstance(spider, RssFeedBaseSpider):
            _item = item.copy()
            pub_date_tz = parse_date(_item['pub_date'])
            _item['pub_date'] = pub_date_tz.astimezone(tz=UTC)
            try:
                with self.db.transaction():
                    RssNews.create(**_item)
            except DatabaseError as err:
                spider.log('Raise DatabaseError: {0}'.format(err), level=ERROR)
        return item

from logging import ERROR
import importlib
from peewee import DatabaseError
from scrapy import Spider
from .settings import SQLITE_DB_PLACE
from .models import get_database, create_tables, RssNews


class SQLiteBasePipeline:

    def __init__(self, db_place=None):
        if db_place is None:
            db_place = SQLITE_DB_PLACE
        self.db = get_database(db_place)
        create_tables()

    def open_spider(self, spider: Spider):
        self.db.connect()

    def close_spider(self, spider: Spider):
        self.db.close()


class RssFeedPipeline(SQLiteBasePipeline):

    def process_item(self, item: dict, spider: Spider):
        if spider.name == 'rss_feed':
            try:
                with self.db.transaction():
                    RssNews.create(**item)
            except DatabaseError as err:
                spider.log('Raise DatabaseError: %(err)s', level=ERROR, err=err)
        return item

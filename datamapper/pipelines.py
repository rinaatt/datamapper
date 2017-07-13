from pytz import UTC
from logging import ERROR
from dateutil.parser import parse as parse_date
from peewee import DatabaseError
from scrapy import Spider
from .spiders import RssFeedBaseSpider
from .settings import SQLITE_DB_PLACE
from .models import RssNews


def get_database():
    from .models import database, create_db_tables
    database.init(SQLITE_DB_PLACE)
    create_db_tables(database)
    return database


class SQLiteBasePipeline:
    conn = None

    def __init__(self, db=None):
        if db is None:
            db = get_database()
        self.db = db

    def open_spider(self, spider: Spider):
        if self.db.is_closed():
            self.db.connect()

    def close_spider(self, spider: Spider):
        if not self.db.is_closed():
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

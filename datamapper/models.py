import peewee as orm
from .settings import SQLITE_DB_PLACE

DB = orm.SqliteDatabase(SQLITE_DB_PLACE)


class BaseModel(orm.Model):

    class Meta:
        database = DB


class RssNews(BaseModel):
    title = orm.CharField(max_length=1000)
    link = orm.CharField(max_length=1000)
    guid = orm.CharField(max_length=1000)
    pub_date = orm.DateTimeField()
    description = orm.TextField()

    class Meta:
        db_table = 'rss_news'


def create_db_tables():
    DB.connect()
    DB.create_tables([RssNews, ], True)
    DB.close()
    return DB

import peewee as orm

database = orm.SqliteDatabase(None)


class BaseModel(orm.Model):

    class Meta:
        database = database


class RssNews(BaseModel):
    title = orm.CharField(max_length=1000)
    link = orm.CharField(max_length=1000)
    guid = orm.CharField(max_length=1000)
    pub_date = orm.DateTimeField()
    description = orm.TextField()

    class Meta:
        db_table = 'rss_news'


def create_db_tables(db):
    db.connect()
    db.create_tables([RssNews, ], True)
    # db.close()

import peewee as orm


def get_database(db_place=None):
    if db_place is None:
        from .settings import SQLITE_DB_PLACE
        db_place = SQLITE_DB_PLACE
    return orm.SqliteDatabase(db_place, threadlocals=True)


class BaseModel(orm.Model):

    class Meta:
        database = get_database()


class RssNews(BaseModel):
    title = orm.CharField(max_length=1000)
    link = orm.CharField(max_length=1000)
    guid = orm.CharField(max_length=1000)
    pub_date = orm.DateTimeField()
    description = orm.TextField()


def create_tables():
    db = get_database()
    db.connect()
    db.create_tables([RssNews, ], True)

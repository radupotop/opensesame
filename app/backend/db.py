from functools import cache

from peewee import Database, SqliteDatabase


@cache
def init_db(path: str) -> Database:
    """
    Singleton to init database from file.
    """
    return SqliteDatabase(path)

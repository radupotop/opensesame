from functools import cache
from pathlib import Path

from peewee import Database, SqliteDatabase


@cache
def init_db(path: str) -> Database:
    """
    Singleton to init database from file.
    """
    if not Path(path).is_file():
        raise RuntimeError('Database file not found')
    return SqliteDatabase(path)

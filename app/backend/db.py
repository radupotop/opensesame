from functools import cache
from pathlib import Path

from peewee import Database, SqliteDatabase


@cache
def get_db(path: str) -> Database:
    if not Path(path).is_file():
        raise RuntimeError('Database file not found')
    return SqliteDatabase(path)

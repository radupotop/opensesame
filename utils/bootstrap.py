from app.db import db
from app.model import Tokens


def bootstrap():
    db.connect(reuse_if_open=True)
    db.create_tables([Tokens])
    db.close()


if __name__ == '__main__':
    bootstrap()

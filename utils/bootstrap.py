from app.db import db
from app.model import LastLogins, Tokens


def bootstrap():
    db.connect(reuse_if_open=True)
    db.create_tables([Tokens, LastLogins])
    db.close()


if __name__ == '__main__':
    bootstrap()

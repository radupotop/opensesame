from app.model import Tokens, db

if __name__ == '__main__':
    db.connect()
    db.create_tables([Tokens])
    db.close()

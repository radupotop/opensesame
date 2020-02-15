import hashlib
from typing import Tuple
from datetime import datetime, timedelta

from app.model import Tokens, db


class Storage:
    def __init__(self):
        self.conn = db.connect(reuse_if_open=True)

    def add_token(self, expiry_days: int = None) -> Tuple:
        _hash = hashlib.sha256(str(datetime.utcnow()).encode()).hexdigest()
        _expires = None

        if expiry_days:
            _expires = datetime.utcnow() + timedelta(days=expiry_days)

        Tokens.insert(value=_hash, expires=_expires).execute()

        return _hash, _expires

    def verify_token(self, value: str) -> bool:
        token = (
            Tokens.select()
            .where(Tokens.value == value)
            .where((Tokens.expires == None) | (Tokens.expires > datetime.utcnow()))
        )
        return token.exists()

    def expire_token(self, value: str) -> bool:
        token = Tokens.delete().where(Tokens.value == value).execute()
        return bool(token)

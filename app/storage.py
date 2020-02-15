from datetime import datetime, timedelta
from typing import Tuple
from uuid import uuid4

from app.db import db
from app.model import Tokens


class Storage:
    def __init__(self):
        self.conn = db.connect(reuse_if_open=True)

    def add_token(self, expiry_days: int = None) -> Tuple:
        _value = str(uuid4())
        _expires = None

        if expiry_days:
            _expires = datetime.utcnow() + timedelta(days=expiry_days)

        Tokens.insert(value=_value, expires=_expires).execute()

        return _value, _expires

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

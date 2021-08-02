from datetime import datetime, timedelta
from typing import Tuple
from uuid import uuid4

from app.db import db
from app.model import AccessRequests, Tokens
from app.utils import parse_ip


class Storage:
    """
    Storage abstracts away common operations done on the SQL db.
    """

    def __init__(self):
        self.conn = db.connect(reuse_if_open=True)

    def _today(self):
        return datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

    def add_token(self, expiry_days: int = None) -> Tuple:
        """
        Generate UUID4 tokens for now.
        An expiry_days value of 0 will render the token expired.
        """
        _value = uuid4()
        _expires = None

        if expiry_days:
            _expires = self._today() + timedelta(days=expiry_days)

        Tokens.insert(value=_value, expires=_expires).execute()

        return _value, _expires

    def verify_token(self, value: str) -> Tuple[bool, int]:
        token = (
            Tokens.select()
            .where(Tokens.value == value)
            .where((Tokens.expires == None) | (Tokens.expires > datetime.utcnow()))
        )
        return token.exists(), token.id

    def expire_token(self, value: str) -> bool:
        """
        Expire the token but keep the entry.
        """
        token = (
            Tokens.update({Tokens.expires: self._today()})
            .where(Tokens.value == value)
            .execute()
        )
        return bool(token)

    def delete_token(self, value: str) -> bool:
        """
        This is meant to run as a periodic cleanup function.
        """
        token = Tokens.delete().where(Tokens.value == value).execute()
        return bool(token)

    def log_access_request(self, src_ip: str, token: Tokens):
        """
        Add an entry to the access request log.
        """
        return AccessRequests.insert(
            timestamp=datetime.utcnow(),
            src_ip=parse_ip(src_ip),
            token=token,
        ).execute()

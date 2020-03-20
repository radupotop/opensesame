from datetime import datetime, timedelta
import pytest

from app.storage import Storage
from utils.bootstrap import bootstrap

bootstrap()
storage = Storage()


class TestToken:
    @pytest.fixture(scope='class')
    def new_token(self):
        return storage.add_token()

    def test_add_token(self, new_token):
        token, expires = new_token
        assert token
        assert not expires

    def test_verify_expire_token(self, new_token):
        token, expires = new_token
        assert storage.verify_token(token)
        assert storage.expire_token(token)

    def test_expired_token(self, new_token):
        token, expires = new_token
        assert not storage.verify_token(token)


class TestTokenVerifyExpired:
    @pytest.fixture(scope='class')
    def new_token(self):
        return storage.add_token(expiry_days=3)

    def test_add_token(self, new_token):
        token, expires = new_token
        assert token
        assert expires > datetime.utcnow()

    def test_verify_token_valid(self, new_token):
        token, expires = new_token
        assert storage.verify_token(token)

    @pytest.mark.freeze_time(datetime.utcnow() + timedelta(days=4))
    def test_verify_token_expired(self, new_token):
        token, expires = new_token
        assert not storage.verify_token(token)

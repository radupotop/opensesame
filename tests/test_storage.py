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
        assert not storage.expire_token(token)

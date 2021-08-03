import pytest
from api.api import application
from app.storage import Storage
from utils.bootstrap import create_db
from werkzeug.test import Client

create_db()
storage = Storage()


class TestAPI:
    @pytest.fixture(scope='class')
    def new_token(self):
        return storage.add_token()

    def setup_class(self):
        self.client = Client(application)

    def test_valid_request(self, new_token):
        token_value, expires = new_token
        response = self.client.get(f'/?token={token_value}')
        assert response.status_code == 201

    def test_bad_request(self):
        response = self.client.get(f'/?token=BADTOKEN')
        assert response.status_code == 403

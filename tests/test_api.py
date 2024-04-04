import iptc
import pytest
from werkzeug.test import Client

from api.api import application
from app.config import ConfigReader
from app.iptables import IPTables
from app.storage import Storage
from utils.bootstrap import create_db

create_db()
storage = Storage()


class TestAPI:
    def setup_class(self):
        cfg = ConfigReader()
        ipt = IPTables(cfg)
        ipt.setup_whitelist_chain()
        self.client = Client(application)
        self.token = storage.add_token()

    def teardown_class(self):
        iptc.easy.delete_chain('filter', 'opensesame', flush=True)

    def test_valid_request(self):
        token_value, expires = self.token
        response = self.client.get(f'/?token={token_value}')
        assert response.status_code == 201

    def test_valid_request_existing_ip(self):
        token_value, expires = self.token
        response = self.client.get(f'/?token={token_value}')
        assert response.status_code == 200

    def test_bad_request(self):
        response = self.client.get('/?token=BADTOKEN')
        assert response.status_code == 403

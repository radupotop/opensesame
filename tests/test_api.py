import iptc
from werkzeug.test import Client

from app.api.http import application
from app.backend.config import ConfigReader
from app.backend.iptables import IPTables
from app.backend.storage import Storage
from app.bootstrap.bootstrap import create_db

create_db()
storage = Storage()


class TestAPI:
    def setup_class(self):
        self.cfg = ConfigReader()
        ipt = IPTables(self.cfg)
        ipt.setup_whitelist_chain()
        self.client = Client(application)
        self.token = storage.add_token()

    def teardown_class(self):
        iptc.easy.delete_chain(iptc.Table.FILTER, self.cfg.chain, flush=True)

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

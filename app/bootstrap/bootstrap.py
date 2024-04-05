from app.backend.config import ConfigReader
from app.backend.db import db
from app.backend.iptables import IPTables
from app.backend.model import AccessRequests, Tokens


def create_db():
    db.connect(reuse_if_open=True)
    db.create_tables([Tokens, AccessRequests])
    db.close()


def create_chains():
    cfg = ConfigReader()
    ipt = IPTables(cfg)
    ipt.setup_whitelist_chain()
    ipt.setup_input_chain(set_policy_drop=cfg.set_input_policy_drop)


if __name__ == '__main__':
    create_db()
    create_chains()

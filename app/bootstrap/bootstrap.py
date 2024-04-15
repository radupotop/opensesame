from app.api import init
from app.backend.model import AccessRequests, Tokens
from peewee import Database


def create_db(db: Database):
    db.connect(reuse_if_open=True)
    db.create_tables([Tokens, AccessRequests])
    db.close()


def create_chains(ipt, cfg):
    ipt.setup_whitelist_chain()
    ipt.setup_input_chain(set_policy_drop=cfg.set_input_policy_drop)


if __name__ == '__main__':
    storage, ipt, cfg = init()
    create_db(storage.get_db())
    create_chains(ipt, cfg)

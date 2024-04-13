from functools import cache

from app.backend.config import ConfigReader
from app.backend.db import init_db
from app.backend.iptables import IPTables
from app.backend.storage import Storage


@cache
def init(config_file='config.yml') -> tuple[ConfigReader, Storage, IPTables]:
    """
    Singleton init function to be reused across the app.
    """
    cfg = ConfigReader(config_file)
    active_db = init_db(cfg.database_path)
    storage = Storage(active_db)
    ipt = IPTables(cfg)
    return cfg, storage, ipt

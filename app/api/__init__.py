from app.backend.config import ConfigReader
from app.backend.db import get_db
from app.backend.iptables import IPTables
from app.backend.storage import Storage
from functools import cache


@cache
def init(config_file='config.yml') -> tuple[ConfigReader, Storage, IPTables]:
    """
    Singleton init function to be reused across the app.
    """
    cfg = ConfigReader(config_file)
    active_db = get_db(cfg.database_path)
    storage = Storage(active_db)
    ipt = IPTables(cfg)
    return cfg, storage, ipt

from functools import cache

from app.backend.config import ConfigReader
from app.backend.db import init_db
from app.backend.iptables import IPTables
from app.backend.storage import Storage


@cache
def init(
    config_file='config.yml',
    with_ipt=True,
) -> tuple[Storage, IPTables | None, ConfigReader]:
    """
    Singleton init function to be reused across the app.
    Have the option to init without IPTables, since they
    require extended privileges.
    """
    cfg = ConfigReader(config_file)
    active_db = init_db(cfg.database_path)
    storage = Storage(active_db)
    ipt = IPTables(cfg) if with_ipt else None
    return storage, ipt, cfg

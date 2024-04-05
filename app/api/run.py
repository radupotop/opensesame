from app.backend.config import ConfigReader
from app.backend.iptables import IPTables

from app.api.http import run_main

if __name__ == '__main__':
    cfg = ConfigReader()
    ipt = IPTables(cfg)

    # ipt.get_chain()
    # ipt.add_rule('192.168.1.6')
    run_main(cfg)

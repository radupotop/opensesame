from app.config import ConfigReader
from app.iptables import IPTables

from api.api import run_main

if __name__ == '__main__':
    cfg = ConfigReader()
    ipt = IPTables(cfg)

    # ipt.get_chain()
    # ipt.add_rule('192.168.1.6')
    run_main(cfg)

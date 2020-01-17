from config import ConfigReader
from iptables import IPTables

if __name__ == '__main__':
    cfg = ConfigReader()
    ipt = IPTables(cfg)

    # Used one time for the initial setup.
    # ipt.setup_chain()

    ipt.get_chain()
    ipt.add_rule('192.168.1.6')

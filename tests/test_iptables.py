import iptc

from app.config import ConfigReader
from app.iptables import IPTables


class TestIPTables:
    def setup_class(self):
        self.cfg = ConfigReader()
        self.ipt = IPTables(self.cfg)
        self.filter_table = iptc.Table(iptc.Table.FILTER)

    def test_setup_chain(self):
        self.ipt.setup_chain()

        chain_names = [c.name for c in self.filter_table.chains]

        assert self.cfg.CHAIN in chain_names
        # import ipdb; ipdb.set_trace()

        input_rule0 = self.filter_table.chains[0].rules[0].matches[0]

        assert self.cfg.SSH_PORT == input_rule0.parameters['dport']
        assert 'tcp' == input_rule0.name

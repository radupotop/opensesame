import iptc
import pytest

from app.config import ConfigReader
from app.iptables import IPTables


class TestIPTables:
    def setup_class(self):
        self.cfg = ConfigReader()
        self.ipt = IPTables(self.cfg)
        self.filter_table = iptc.Table(iptc.Table.FILTER)

    def test_setup_chain(self):
        self.ipt.setup_chain()

    def test_initial_chain_added(self):
        chain_names = [c.name for c in self.filter_table.chains]

        assert self.cfg.CHAIN in chain_names

    def test_chain_policy(self):
        assert self.filter_table.chains[0].name == 'INPUT'
        assert self.filter_table.chains[0].get_policy().name == iptc.Policy.DROP

    def test_rule_match(self):
        matches0 = self.filter_table.chains[0].rules[0].matches[0]
        assert self.cfg.SSH_PORT == matches0.parameters['dport']
        assert 'tcp' == matches0.name

    def test_add_good_rule(self):
        assert self.ipt.add_rule('192.168.1.1')

    def test_add_bad_rule(self):
        with pytest.raises(ValueError):
            self.ipt.add_rule('192.168.x.x')

    def test_find_rule(self):
        assert self.ipt.add_rule('192.168.1.2')
        assert self.ipt.find_rule('192.168.1.2')

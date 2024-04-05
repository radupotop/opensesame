import iptc
import pytest
from app.config import ConfigReader
from app.exceptions import ParseIPError
from app.iptables import IPTables
from app.utils import parse_port


class TestIPTables:
    def setup_class(self):
        self.cfg = ConfigReader()
        self.ipt = IPTables(self.cfg)
        self.filter_table = iptc.Table(iptc.Table.FILTER)

    def test_setup_chain(self):
        self.ipt.setup_whitelist_chain()
        self.ipt.setup_input_chain(set_policy_drop=True)

    def test_initial_chain_added(self):
        chain_names = [c.name for c in self.filter_table.chains]

        assert self.cfg.chain in chain_names

    def test_chain_policy(self):
        assert self.filter_table.chains[0].name == 'INPUT'
        assert self.filter_table.chains[0].get_policy().name == iptc.Policy.DROP

    def test_rule_match(self):
        matches0 = self.filter_table.chains[0].rules[0].matches[0]
        port, proto = parse_port(self.cfg.ports[0])
        assert port == matches0.parameters['dport']
        assert proto == matches0.name

    def test_add_good_rule(self):
        assert self.ipt.add_rule('192.168.1.1')

    def test_add_bad_rule(self):
        with pytest.raises(ParseIPError):
            self.ipt.add_rule('192.168.x.x')

    def test_has_rule(self):
        assert self.ipt.add_rule('192.168.1.2')
        assert self.ipt.has_rule('192.168.1.2')

    def test_delete_rule(self):
        ip = '192.168.1.19'
        assert self.ipt.add_rule(ip)
        assert self.ipt.has_rule(ip)
        assert self.ipt.delete_rule(ip)
        assert not self.ipt.has_rule(ip)
        assert not self.ipt.delete_rule(ip)

from ipaddress import ip_address

import iptc
from app.config import ConfigReader


class IPTables:
    """
    Wrapper for the iptc class.
    """

    def __init__(self, config: ConfigReader):
        self.cfg = config

    def setup_chain(self):
        """
        Create the initial chain.
        """
        filter_table = iptc.Table(iptc.Table.FILTER)
        self.chain = filter_table.create_chain(self.cfg.CHAIN)

        input_chain = iptc.Chain(filter_table, 'INPUT')

        input_rule = iptc.Rule()
        input_rule.protocol = 'tcp'

        input_match = iptc.Match(input_rule, 'tcp')
        input_match.dport = str(self.cfg.SSH_PORT)
        input_rule.add_match(input_match)

        input_rule.target = iptc.Target(input_rule, self.cfg.CHAIN)

        input_chain.append_rule(input_rule)
        input_chain.set_policy(iptc.Policy.DROP)

    def get_chain(self):
        """
        Get target chain.
        """
        filter_table = iptc.Table(iptc.Table.FILTER)
        self.chain = iptc.Chain(filter_table, self.cfg.CHAIN)

    def add_rule(self, src_ip: str):
        """
        Create rule to allow inbound traffic from <SRC IP>.
        """
        rule = iptc.Rule()
        rule.src = str(ip_address(src_ip))
        rule.target = iptc.Target(rule, iptc.Policy.ACCEPT)
        self.chain.insert_rule(rule)
        return True

from ipaddress import ip_address
from typing import List

import iptc
from app.config import ConfigReader


class IPTables:
    """
    Wrapper for the iptc class.
    """

    def __init__(self, config: ConfigReader):
        self.config = config
        self.filter_table = iptc.Table(iptc.Table.FILTER)

    def _parse_ip(self, ip_addr: str) -> str:
        return str(ip_address(ip_addr))

    def setup_chain(self):
        """
        Create the opensesame chain which will hold all the whitelist rules.
        Append a rule to the INPUT chain to jump to Opensesame for all packets
        matching the SSH destination port.
        Finally set the INPUT chain policy to DROP.
        """
        self.chain = self.filter_table.create_chain(self.config.CHAIN)
        input_chain = iptc.Chain(self.filter_table, 'INPUT')

        input_rule = iptc.Rule()
        input_rule.protocol = 'tcp'

        input_match = iptc.Match(input_rule, 'tcp')
        input_match.dport = str(self.config.SSH_PORT)
        input_rule.add_match(input_match)

        input_rule.target = iptc.Target(input_rule, self.config.CHAIN)

        input_chain.append_rule(input_rule)
        input_chain.set_policy(iptc.Policy.DROP)

    def get_chain(self):
        """
        Get the opensesame chain.
        """
        self.chain = iptc.Chain(self.filter_table, self.config.CHAIN)

    def add_rule(self, src_ip: str) -> bool:
        """
        Create rule to allow inbound traffic from <SRC IP>.
        """
        rule = iptc.Rule()
        rule.src = self._parse_ip(src_ip)
        rule.target = iptc.Target(rule, iptc.Policy.ACCEPT)
        self.chain.insert_rule(rule)
        return True

    def find_rule(self, src_ip: str) -> List:
        """
        Find a src IP address in the opensesame chain.
        """
        ipaddr = self._parse_ip(src_ip)
        found = [rule for rule in self.chain.rules if ipaddr == rule.src.split('/')[0]]
        return found

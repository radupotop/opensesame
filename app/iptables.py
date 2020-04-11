from ipaddress import ip_address, ip_network

import iptc
from app.config import ConfigReader


class IPTables:
    """
    Wrapper for the iptc class.
    """

    def __init__(self, config: ConfigReader):
        self.config = config
        self.filter_table = iptc.Table(iptc.Table.FILTER)

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

    def add_rule(self, src_ip: str):
        """
        Create rule to allow inbound traffic from <SRC IP>.
        """
        rule = iptc.Rule()
        rule.src = str(ip_address(src_ip))
        rule.target = iptc.Target(rule, iptc.Policy.ACCEPT)
        self.chain.insert_rule(rule)
        return True

    def _get_ip_address(self, net_addr):
        """
        Get IP address from Network address.
        """
        return str(ip_network(net_addr).network_address)

    def find_rule(self, ipaddr: str):
        """
        Find an IP address in the opensesame chain.
        """
        found = [
            rule for rule in self.chain.rules if ipaddr == self._get_ip_address(rule.src)
        ]
        return found

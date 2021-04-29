from ipaddress import ip_address
from typing import Tuple

import iptc

from app.config import ConfigReader
from app.logging import get_logger

log = get_logger(__name__)


class IPTables:
    """
    Wrapper for the iptc class.
    """

    def __init__(self, config: ConfigReader):
        self.config = config
        self.filter_table = iptc.Table(iptc.Table.FILTER)

    def _parse_ip(self, ip_addr: str) -> str:
        return str(ip_address(ip_addr))

    def _parse_port(self, entry: str) -> Tuple[str, str]:
        """
        Parse a port:protocol entry from the config.
        """
        port, protocol = entry.split(':', 1)
        return port, protocol

    def setup_chain(self):
        """
        Create the opensesame chain which will hold all the whitelist rules.
        Append a rule to the INPUT chain to jump to Opensesame for all packets
        matching the SSH destination port.
        Finally set the INPUT chain policy to DROP.
        """
        self.chain = self.filter_table.create_chain(self.config.chain)
        input_chain = iptc.Chain(self.filter_table, 'INPUT')

        for entry in self.config.ports:
            port, protocol = self._parse_port(entry)
            input_rule = self.allow_inbound_port(port, protocol)
            input_chain.append_rule(input_rule)
            log.info('Added INPUT chain rule for %s:%s', port, protocol)

        if self.config.set_input_policy_drop:
            log.warning('Setting the INPUT chain Policy to DROP')
            input_chain.set_policy(iptc.Policy.DROP)

    def get_chain(self):
        """
        Get the opensesame chain.
        """
        self.chain = iptc.Chain(self.filter_table, self.config.chain)

    def allow_inbound_port(self, port: str, protocol: str = 'all') -> iptc.Rule:
        """
        Add inbound rule for port:protocol.
        iptables -p tcp -m tcp --dport 22 -j opensesame
        """
        input_rule = iptc.Rule()
        input_rule.protocol = protocol

        rule_match = iptc.Match(input_rule, protocol)
        rule_match.dport = str(port)
        input_rule.add_match(rule_match)
        input_rule.target = iptc.Target(input_rule, self.config.chain)
        log.debug('Built inbound rule for %s,%s', port, protocol)

        return input_rule

    def add_rule(self, src_ip: str) -> bool:
        """
        Create rule to allow inbound traffic from <SRC IP>.
        """
        rule = iptc.Rule()
        rule.src = self._parse_ip(src_ip)
        rule.target = iptc.Target(rule, iptc.Policy.ACCEPT)
        self.chain.insert_rule(rule)
        log.info('Allowing inbound traffic from SRC IP: %s', src_ip)
        return True

    def find_rule(self, src_ip: str) -> bool:
        """
        Find a src IP address in the opensesame chain.
        """
        ipaddr = self._parse_ip(src_ip)
        found = [rule for rule in self.chain.rules if ipaddr == rule.src.split('/')[0]]
        return bool(found)

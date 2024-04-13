import iptc

from app.backend.config import ConfigReader
from app.backend.logging import get_logger
from app.backend.utils import parse_ip, parse_port

log = get_logger(__name__)


class IPTables:
    """
    Wrapper for the iptc class.
    """

    def __init__(self, config: ConfigReader):
        self.config = config
        self.filter_table = iptc.Table(iptc.Table.FILTER)

    def setup_whitelist_chain(self):
        """
        Create the opensesame chain which will hold all the whitelist rules.
        This is a one-time operation.
        """
        log.info('Creating the whitelist chain: %s', self.config.chain)
        self.chain = self.filter_table.create_chain(self.config.chain)

    def setup_input_chain(self, set_policy_drop=False):
        """
        Append a rule to the INPUT chain to jump to the whitelist chain for
        all the packets matching the destination ports & protocols.
        Finally set the INPUT chain policy to DROP.
        """
        input_chain = iptc.Chain(self.filter_table, 'INPUT')
        log.info(
            'Adding the INPUT chain rules. Setting policy to DROP=%s',
            set_policy_drop,
        )

        for entry in self.config.ports:
            port, protocol = parse_port(entry)
            input_rule = self.build_inbound_rule(port, protocol)
            input_chain.append_rule(input_rule)

        # Add rule for allowing the opensesame API
        accept_self = self.build_inbound_rule(
            self.config.api_port, 'tcp', always_accept=True
        )
        input_chain.append_rule(accept_self)

        if set_policy_drop:
            log.warning('Setting the INPUT chain Policy to DROP')
            input_chain.set_policy(iptc.Policy.DROP)

    def get_chain(self):
        """
        Get the opensesame chain.
        """
        self.chain = iptc.Chain(self.filter_table, self.config.chain)

    def build_inbound_rule(
        self, port: str, protocol: str, always_accept: bool = False
    ) -> iptc.Rule:
        """
        Build an inbound rule for port:protocol which will jump to the whitelist chain.

        Example:
            iptables -A INPUT -p tcp -m tcp --dport 22 -j opensesame
        """
        input_rule = iptc.Rule()
        input_rule.protocol = protocol

        rule_match = iptc.Match(input_rule, protocol)
        rule_match.dport = str(port)
        input_rule.add_match(rule_match)
        jump_to = iptc.Policy.ACCEPT if always_accept else self.config.chain
        input_rule.target = iptc.Target(input_rule, jump_to)
        log.info('Creating inbound rule for: %s, %s, %s', port, protocol, jump_to)
        return input_rule

    def add_rule(self, src_ip: str) -> bool:
        """
        Create rule to accept inbound traffic from <SRC IP>.

        Example:
            iptables -A opensesame -s SRC_IP -j ACCEPT
        """
        if not hasattr(self, 'chain'):
            self.get_chain()
        rule = iptc.Rule()
        rule.src = parse_ip(src_ip)
        rule.target = iptc.Target(rule, iptc.Policy.ACCEPT)
        self.chain.append_rule(rule)
        log.info('Allowing inbound traffic from SRC IP: %s', src_ip)
        return True

    def _lookup_rules(self, src_ip: str) -> list[iptc.Rule]:
        ipaddr = parse_ip(src_ip)
        return [rule for rule in self.chain.rules if ipaddr == rule.src.split('/')[0]]

    def has_rule(self, src_ip: str) -> bool:
        """
        Find a src IP address in the opensesame chain.
        """
        found = bool(self._lookup_rules(src_ip))
        log.info('Found rule for IP: %s, %s', src_ip, found)
        return found

    def delete_rule(self, src_ip: str) -> bool:
        """
        Drop a rule from the opensesame chain.
        """
        found_rules = self._lookup_rules(src_ip)
        for rule in found_rules:
            self.chain.delete_rule(rule)
        count = len(found_rules)
        log.info('Deleted %s rules for IP: %s', count, src_ip)
        return bool(count)

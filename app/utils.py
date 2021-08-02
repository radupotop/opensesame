import re
from ipaddress import ip_address
from logging import get_logger
from typing import Optional, Tuple

log = get_logger(__name__)


UUID_REGEX = re.compile('^\w{8}-\w{4}-\w{4}-\w{4}-\w{12}$')


def parse_ip(ip_addr: str) -> Optional[str]:
    try:
        resp_ip = str(ip_address(ip_addr))
    except ValueError:
        log.warning('Could not parse IP %s', ip_addr)
        resp_ip = None
    return resp_ip


def parse_port(entry: str) -> Tuple[str, str]:
    """
    Parse a port:protocol entry from the config.
    """
    port, protocol = entry.split(':', 1)
    return port, protocol


def is_valid_uuid4(token: str) -> bool:
    return bool(UUID_REGEX.findall(str(token)))

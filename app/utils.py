import re
from ipaddress import ip_address
from typing import Optional, Tuple

from app.exceptions import ParseIPError
from app.logging import get_logger

log = get_logger(__name__)


UUID_REGEX = re.compile(r'^\w{8}-\w{4}-\w{4}-\w{4}-\w{12}$')


def parse_ip(ip_addr: str) -> str:
    try:
        resp_ip = str(ip_address(ip_addr))
    except ValueError as e:
        raise ParseIPError(e)
    return resp_ip


def parse_port(entry: str) -> Tuple[str, str]:
    """
    Parse a port:protocol entry from the config.
    """
    port, protocol = entry.split(':', 1)
    return port, protocol


def is_valid_uuid4(token: str) -> bool:
    return bool(UUID_REGEX.findall(str(token)))


def is_valid_ip(ip_addr: str) -> Optional[str]:
    try:
        resp_ip = parse_ip(ip_addr)
    except ParseIPError:
        resp_ip = None
    return resp_ip

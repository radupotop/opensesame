import socket
from ipaddress import ip_address
from typing import Tuple
from uuid import UUID

from app.exceptions import ParseIPError
from app.logging import get_logger

log = get_logger(__name__)


def parse_ip(ip_addr: str) -> str:
    try:
        resp_ip = str(ip_address(ip_addr))
    except ValueError as e:
        raise ParseIPError(e)
    return resp_ip


def resolve_hostname(hostname: str) -> str:
    try:
        resolved_ip = socket.gethostbyname(hostname)
    except socket.error as e:
        raise ParseIPError(e)
    return resolved_ip


def parse_port(entry: str) -> Tuple[str, str]:
    """
    Parse a port:protocol entry from the config.
    """
    port, protocol = entry.split(':', 1)
    return port, protocol


def is_valid_uuid(token: str) -> bool:
    try:
        UUID(token)
        isvalid = True
    except (ValueError, TypeError):
        isvalid = False
    return isvalid


def is_valid_ip(ip_addr: str) -> bool:
    try:
        resp_ip = parse_ip(ip_addr)
    except ParseIPError:
        resp_ip = False
    return bool(resp_ip)


def parse_host(hostnameport: str) -> Tuple[str, str]:
    """
    Parse a hostname:port pair from the request headers.
    """
    hp = hostnameport.split(':', 1)
    if len(hp) == 1:
        return hp[0], ''
    return hp

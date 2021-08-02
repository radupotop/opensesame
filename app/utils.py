from ipaddress import ip_address
from re import compile

UUID_REGEX = re.compile('^\w{8}-\w{4}-\w{4}-\w{4}-\w{12}$')


def parse_ip(ip_addr: str) -> str:
    return str(ip_address(ip_addr))


def parse_port(entry: str) -> Tuple[str, str]:
    """
    Parse a port:protocol entry from the config.
    """
    port, protocol = entry.split(':', 1)
    return port, protocol


def is_valid_uuid4(token: str) -> bool:
    return bool(UUID_REGEX.findall(str(token)))

from http import HTTPStatus as hs

from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response

from app.backend.config import ConfigReader
from app.backend.iptables import IPTables
from app.backend.logging import get_logger
from app.backend.storage import Storage
from app.backend.utils import is_valid_ip, is_valid_uuid, parse_host, resolve_hostname

storage = Storage()
log = get_logger(__name__)


def build_response(message: str, code: int):
    """
    Build JSON response.
    """
    return Response(message, content_type='application/json', status=code)


def bad_token():
    return build_response('"Could not verify access token."', code=hs.FORBIDDEN)


@Request.application
def application(request):
    """
    Define the WSGI application to be run by the server.
    """
    if request.path.startswith('/favicon'):
        return build_response(None, code=hs.NO_CONTENT)

    cfg = ConfigReader()
    ipt = IPTables(cfg)

    token = request.args.get('token')
    hostname, _ = parse_host(request.host)
    src_ip = resolve_hostname(request.remote_addr or hostname)

    if not (is_valid_uuid(token) and is_valid_ip(src_ip)):
        log.warning('Invalid Token <%s> or SRC IP <%s>', token, src_ip)
        return bad_token()

    token_instance = storage.verify_token(token)

    if token_instance:
        ipt.get_chain()
        if not ipt.has_rule(src_ip):
            ipt.add_rule(src_ip)
            storage.log_access_request(src_ip, token_instance)
            log.info('Allowing inbound traffic from new IP: %s', src_ip)
            return build_response(
                f'"Allowing inbound traffic from new IP: {src_ip}"', code=hs.CREATED
            )
        log.info('Allowing inbound traffic from existing IP: %s', src_ip)
        return build_response(
            f'"Allowing inbound traffic from existing IP: {src_ip}"', code=hs.OK
        )
    else:
        log.warning('Invalid Token: %s', token)
        return bad_token()


def run_main(cfg):
    """
    Convenience method. Run a simple server and load the app.
    """
    log.info('Started OpenSesame %s:%s', cfg.api_host, cfg.api_port)
    run_simple(cfg.api_host, int(cfg.api_port), application)

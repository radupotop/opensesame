import json
from time import sleep

from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response

from app.config import ConfigReader
from app.iptables import IPTables
from app.logging import get_logger
from app.storage import Storage
from app.utils import is_valid_ip, is_valid_uuid4

storage = Storage()
log = get_logger(__name__)


def build_response(message: str, code: int):
    """
    Build JSON response.
    """
    return Response(message, content_type='application/json', status=code)


def bad_token():
    return build_response('"Could not verify access token."', code=403)


@Request.application
def application(request):
    """
    Define the WSGI application to be run by the server.
    """
    cfg = ConfigReader()
    ipt = IPTables(cfg)

    token = request.args.get('token')
    src_ip = str(request.host)

    if not (is_valid_uuid4(token) and is_valid_ip(src_ip)):
        log.warning('Invalid Token <%s> or SRC IP <%s>', token, src_ip)
        return bad_token()

    token_is_valid, token_id = storage.verify_token(token)

    if token_is_valid:
        if not ipt.find_rule(src_ip):
            ipt.add_rule(src_ip)
            storage.log_access_request(src_ip, token_id)
            log.info('Allowing inbound traffic from new IP: %s', src_ip)
            return build_response(
                f'"Allowing inbound traffic from new IP: {src_ip}"', code=201
            )
        log.info('Allowing inbound traffic from existing IP: %s', src_ip)
        return build_response(
            f'"Allowing inbound traffic from existing IP: {src_ip}"', code=200
        )
    else:
        log.warning('Invalid Token: %s', token)
        return bad_token()


def run_main(cfg):
    """
    Convenience method. Run a simple server and load the app.
    """
    run_simple(cfg.api_host, int(cfg.api_port), application)

from http import HTTPStatus as hs

from werkzeug.wrappers import Request, Response

from app.api import init
from app.backend.logging import get_logger
from app.backend.utils import is_valid_ip, is_valid_uuid, parse_host, resolve_hostname

log = get_logger(__name__)


def build_response(message: str, code: int):
    """
    Build JSON response.
    """
    return Response(message, content_type='application/json', status=code)


def bad_token():
    return build_response('"Could not verify access token."', code=hs.FORBIDDEN)


def expired_token():
    return build_response('"Token has expired."', code=hs.FORBIDDEN)


@Request.application
def application(request):
    """
    Define the WSGI application to be run by the server.
    """
    if request.path.startswith('/favicon'):
        return build_response(None, code=hs.NO_CONTENT)

    token = request.args.get('token')
    hostname, _ = parse_host(request.host)
    src_ip = resolve_hostname(request.remote_addr or hostname)

    if not (is_valid_uuid(token) and is_valid_ip(src_ip)):
        log.warning('Invalid Token <%s> or SRC IP <%s>', token, src_ip)
        return bad_token()

    storage, ipt, _ = init()
    token_instance = storage.get_token(token)

    if token_instance and token_instance.is_valid:
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
    elif token_instance:
        log.warning('Token expired: %s', token)
        # Try to cleanup iptables
        ipt.delete_rule(src_ip)
        return expired_token()
    else:
        log.warning('Invalid Token: %s', token)
        return bad_token()

import json
from time import sleep

from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response

from app.storage import Storage
from app.config import ConfigReader
from app.iptables import IPTables

storage = Storage()


def build_response(message: str, code: int):
    """
    Build JSON response.
    """
    return Response(message, content_type='application/json', status=code)


@Request.application
def application(request):
    """
    Define the WSGI application to be run by the server.
    """
    cfg = ConfigReader()
    ipt = IPTables(cfg)

    token = request.args.get('token')
    src_ip = str(request.host)

    if token and storage.verify_token(token):
        if not ipt.find_rule(src_ip):
            ipt.add_rule(src_ip)
            return build_response(
                f'"Allowing inbound traffic from new IP: {src_ip}"', code=201
            )
        return build_response(
            f'"Allowing inbound traffic from existing IP: {src_ip}"', code=200
        )
    else:
        return build_response('"Could not verify access token."', code=403)


def run_main(cfg):
    """
    Convenience method. Run a simple server and load the app.
    """
    run_simple(cfg.API_HOST, int(cfg.API_PORT), application)

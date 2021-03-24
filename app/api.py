import json
from time import sleep

from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response

from app.storage import Storage
from app.config import ConfigReader
from app.iptables import IPTables

storage = Storage()


@Request.application
def application(request):
    """
    Define the WSGI application to be run by the server.
    """
    cfg = ConfigReader()
    ipt = IPTables(cfg)

    token = request.args.get('token')
    src_ip = request.host

    if token and storage.verify_token(token):
        if not ipt.find_rule(src_ip):
            ipt.add_rule(src_ip)
        return Response('"OK"', content_type='application/json', status=200)
    else:
        return Response('"ERR"', content_type='application/problem+json', status=400)


def run_main(cfg):
    """
    Convenience method. Run a simple server and load the app.
    """
    run_simple(cfg.API_HOST, int(cfg.API_PORT), application)

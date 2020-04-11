import json
from time import sleep

from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response

from app.storage import Storage

storage = Storage()


@Request.application
def application(request):
    """
    Define the WSGI application to be run by the server.
    """

    token = request.args.get('token')
    src_ip = request.host

    if token and storage.verify_token(token):
        return Response('"OK"', content_type='application/json', status=200)
    else:
        return Response('"ERR"', content_type='application/problem+json', status=400)


def run_main(cfg):
    """
    Convenience method. Run a simple server and load the app.
    """
    run_simple(cfg.API_HOST, int(cfg.API_PORT), application)

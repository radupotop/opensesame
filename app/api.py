import json
from time import sleep

from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response


@Request.application
def application(request):

    token = request.args.get('token')
    src_ip = request.host

    if token:
        return Response('"OK"', content_type='application/json', status=200)
    else:
        return Response('"ERR"', content_type='application/problem+json', status=400)


def run_main(cfg):
    run_simple(cfg.API_HOST, int(cfg.API_PORT), application)

from werkzeug.serving import run_simple

from app.api.web import application
from app.backend.config import ConfigReader
from app.backend.logging import get_logger

log = get_logger('app.api.run')


def run_main(cfg):
    """
    Convenience method. Run a simple server and load the app.
    """
    log.info('Started OpenSesame %s:%s', cfg.api_host, cfg.api_port)
    run_simple(cfg.api_host, int(cfg.api_port), application)


if __name__ == '__main__':
    cfg = ConfigReader()
    run_main(cfg)

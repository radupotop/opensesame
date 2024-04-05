import logging


logging.basicConfig()


def get_logger(name: str):
    log = logging.getLogger(name)
    log.setLevel(logging.INFO)
    return log

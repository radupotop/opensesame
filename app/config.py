from configparser import ConfigParser


class ConfigReader:
    def __init__(self):
        cfg = ConfigParser()
        cfg.read('config.ini')
        for k, v in cfg.defaults().items():
            setattr(self, str(k).upper(), v)

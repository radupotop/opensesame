from pathlib import Path
import yaml


class ConfigReader:
    def __init__(self):
        p = Path('config.yml')
        cfg = yaml.safe_load(p.read_bytes())
        for k, v in cfg.items():
            setattr(self, k, v)

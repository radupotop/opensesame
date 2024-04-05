from pathlib import Path

import yaml


class ConfigReader:
    def __init__(self):
        raw_yaml = Path('config.yml').read_text()
        config_file = yaml.safe_load(raw_yaml)
        for k, v in config_file.items():
            setattr(self, str(k), v)

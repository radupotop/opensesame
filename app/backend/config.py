from pathlib import Path

import yaml


class YamlConfigReader:
    def __init__(self, filename='config.yml'):
        raw_yaml = Path(filename).read_text()
        config_file = yaml.safe_load(raw_yaml)
        for k, v in config_file.items():
            setattr(self, str(k), v)


class ConfigReader(YamlConfigReader):
    pass

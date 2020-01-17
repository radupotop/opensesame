from app.config import ConfigReader


def test_config():
    cfg = ConfigReader()
    assert hasattr(cfg, 'CHAIN')
    assert hasattr(cfg, 'SSH_PORT')

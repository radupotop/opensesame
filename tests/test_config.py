from app.backend.config import ConfigReader


def test_config():
    cfg = ConfigReader()
    assert hasattr(cfg, 'chain')
    assert hasattr(cfg, 'ports')

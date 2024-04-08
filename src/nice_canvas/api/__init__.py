from pathlib import Path

from .http import Canvas, CanvasClient

__all__ = ["Canvas", "CanvasClient", "get_config_file", "get_client"]


def get_config_file() -> Path:
    from platformdirs import user_config_dir

    return Path(user_config_dir("nice_canvas")) / "config.json"


def get_client(config: Path = None):
    if not config:
        config = get_config_file()

    if not isinstance(config, Path):
        config = Path(config)

    if not config.is_file():
        raise FileNotFoundError("Configuration file not found: {}".format(config))

    import json

    with open(config) as f:
        _config = json.load(f)

    if "canvas" not in _config:
        raise KeyError("Canvas configuration not found in {}".format(config))

    _config = _config["canvas"]

    return CanvasClient(_config["base_url"], _config["token"])

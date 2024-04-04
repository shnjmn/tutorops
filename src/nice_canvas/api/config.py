from collections import namedtuple
from pathlib import Path

from platformdirs import user_config_dir

CONFIG_FILE = Path(user_config_dir("nice_canvas")) / "config.json"


CanvasConfig = namedtuple("CanvasConfig", ["base_url", "token"])


def load_config():
    import json

    if not CONFIG_FILE.is_file():
        return None, {}

    with CONFIG_FILE.open() as f:
        config = json.load(f)

    if "canvas" not in config:
        raise KeyError("Canvas configuration not found in {}".format(CONFIG_FILE))

    canvas = CanvasConfig(**config["canvas"])
    del config["canvas"]

    return canvas, config

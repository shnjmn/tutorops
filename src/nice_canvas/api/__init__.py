from .config import CONFIG_FILE, load_config
from .http import Canvas, CanvasClient

__all__ = ["Canvas", "CanvasClient", "CONFIG_FILE", "config", "get_client"]


_client, config = load_config()


def get_client():
    if not _client:
        raise ValueError("Canvas configuration not found in {}".format(CONFIG_FILE))

    return CanvasClient(_client.base_url, _client.token)

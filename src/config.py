import configparser
import os


CONFIG_PLACEMENT = os.path.expanduser("~/.config/congenial-carnival/config.ini")
STEAM_API_KEY = "steam_api_key"
STEAM_ID = "steam_id"


class Configuration:
    def __init__(self, config):
        self.config = config


def load_config(path=CONFIG_PLACEMENT) -> Configuration:
    config = configparser.ConfigParser()
    try:
        config.read(path)
        keys_to_get = [STEAM_API_KEY, STEAM_ID]
        values = {key: config.get("DEFAULT", key, fallback=None) for key in keys_to_get}
        return Configuration(values)
    except (FileNotFoundError, OSError, configparser.Error) as e:
        print(f"Error loading config: {e}")
        return Configuration({})

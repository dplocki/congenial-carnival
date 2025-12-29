import configparser
import os


CONFIG_PLACEMENT = os.path.expanduser("~/.config/congenial-carnival/config.ini")
DATABASE_FILE_PATH = "database"
STEAM_API_KEY = "steam_api_key"
STEAM_ID = "steam_id"


class Configuration:

    def __init__(self, config, load_error=None):
        self.config = config
        self.load_error = load_error

    def is_loaded(self) -> bool:
        return self.load_error is None

    def get_database_path(self) -> str:
        return self.config.get(DATABASE_FILE_PATH)

    def get_steam_api_key(self) -> str:
        return self.config.get(STEAM_API_KEY)

    def get_steam_id(self) -> str:
        return self.config.get(STEAM_ID)


def load_config(path=CONFIG_PLACEMENT) -> Configuration:
    config = configparser.ConfigParser()
    try:
        config.read(path)
        keys_to_get = [DATABASE_FILE_PATH, STEAM_API_KEY, STEAM_ID]
        values = {key: config.get("DEFAULT", key, fallback=None) for key in keys_to_get}
        return Configuration(values)
    except (FileNotFoundError, OSError, configparser.Error) as e:
        return Configuration({}, load_error=e)

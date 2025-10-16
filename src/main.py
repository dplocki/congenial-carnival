from config import load_config
from steam import SteamGamesApi


if __name__ == "__main__":
    config = load_config().config
    result = SteamGamesApi(config['steam_api_key'], config['steam_id'])
    print(config, result.get_owned_games())


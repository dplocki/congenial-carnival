from config import load_config
from steam import SteamGamesApi
from store import Store


if __name__ == "__main__":
    config = load_config()

    store = Store(config.get_database_path())
    store.migrate_database()
    stored_games = {game["name"]: game for game in store.get_stored_games()}

    stored_games_names = set(stored_games.keys())

    steamClient = SteamGamesApi(config.get_steam_api_key(), config.get_steam_id())
    steam_games = {game["name"]: game for game in steamClient.get_owned_games()}

    steam_games_names = set(steam_games.keys())

    for game_name in steam_games_names - stored_games_names:
        store.add_game(game_name)

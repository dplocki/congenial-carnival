import logging
from config import load_config
from steam import SteamGamesApi
from store import Store

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

    config = load_config()
    logging.info("Configuration loaded")

    store = Store(config.get_database_path())
    store.migrate_database()

    stored_games = {game[1]: game for game in store.get_stored_games()}
    stored_games_names = set(stored_games.keys())
    logging.info("Games loaded from the database")

    steamClient = SteamGamesApi(config.get_steam_api_key(), config.get_steam_id())
    steam_games = {game["name"]: game for game in steamClient.get_owned_games()}
    logging.info("Games loaded from the Steam")

    steam_games_names = set(steam_games.keys())

    for game_name in steam_games_names - stored_games_names:
        logging.info("New game found: %s", game_name)
        store.add_game(game_name)

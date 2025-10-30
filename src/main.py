import logging
from config import load_config
from howlongtobeat import fetch_hltb_time
from steam import SteamGamesApi
from store import Store

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s"
    )

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

    for game_id, game_name, game_required_time in stored_games.values():
        if game_required_time is not None:
            continue

        logging.info("Fetching HLTB time for: %s", game_name)
        value = fetch_hltb_time(game_name)
        if value is not None:
            logging.info("Found HLTB time for %s: %d hours", game_name, value)
            store.update_game_required_time(game_id, value)
        else:
            logging.info("HLTB time not found for: %s", game_name)

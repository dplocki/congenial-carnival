import logging
from commands.refresh_games import RefreshGamesCommand
from services.config import load_config
from services.steam_store import SteamStore
from services.store import Store
from punq import Container


def build_container():
    container = Container()
    container.register(SteamStore)
    container.register(Store)

    return container


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s"
    )

    config = load_config()
    logging.info("Configuration loaded")

    container = build_container()

    # Load games
    container.resolve(RefreshGamesCommand).execute()

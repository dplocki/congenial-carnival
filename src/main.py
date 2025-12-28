import logging
from services.config import load_config
from services.steam import SteamGamesApi
from services.store import Store
from punq import Container


def build_container():
    container = Container()
    container.register(SteamGamesApi)
    container.register(Store, factory=lambda: Store(config.get_database_path()))

    return container


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s"
    )

    config = load_config()
    logging.info("Configuration loaded")

    container = build_container()

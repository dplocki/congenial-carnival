import logging
from commands.refresh_games import RefreshGamesCommand
from services.config import Configuration, load_config
from services.games import Games
from services.steam_store import SteamStore
from services.store import Store
from punq import Container


def build_container(config: Configuration) -> Container:
    container = Container()
    container.register(Games)
    container.register(SteamStore, factory=lambda: SteamStore(config.get_steam_api_key(), config.get_steam_id()))
    container.register(Store, factory=lambda: Store(config.get_database_path()))

    container.register(RefreshGamesCommand)

    return container


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s"
    )

    config = load_config()
    logging.info("Configuration loaded")

    container = build_container(config)

    # Load games
    container.resolve(RefreshGamesCommand).execute()

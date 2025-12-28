import logging
import importlib
import inspect
import pkgutil
from typing import Generator
from commands.refresh_games import RefreshGamesCommand
from services.config import Configuration, load_config
from services.games import Games
from services.steam_store import SteamStore
from services.store import Store
from punq import Container


def get_classes_from(package_name: str) -> Generator[type, None, None]:
    pkg = importlib.import_module(package_name)
    for _, modname, _ in pkgutil.iter_modules(pkg.__path__):
        full_name = f"{package_name}.{modname}"
        mod = importlib.import_module(full_name)
        yield from (
            obj
            for _, obj in inspect.getmembers(mod, inspect.isclass)
            if obj.__module__ == full_name
        )


def build_container(config: Configuration) -> Container:
    container = Container()
    container.register(Games)
    container.register(
        SteamStore,
        factory=lambda: SteamStore(config.get_steam_api_key(), config.get_steam_id()),
    )
    container.register(Store, factory=lambda: Store(config.get_database_path()))

    for command_class in get_classes_from("commands"):
        container.register(command_class)

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

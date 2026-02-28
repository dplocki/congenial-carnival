import logging
import importlib
import inspect
from pathlib import Path
import pkgutil
from typing import Generator
from services.command_bus import CommandBus
from services.config import Configuration, load_config
from services.entries_reducer import EntriesReducer
from services.how_long_to_beat import HowLongToBeat
from services.input_data_loader import InputDataLoader
from services.steam_api import SteamApi
from services.store import Store
from punq import Container


def get_classes_from(package_name: str) -> Generator[type, None, None]:
    pkg = importlib.import_module(package_name)
    for _, mod_name, _ in pkgutil.iter_modules(pkg.__path__):
        full_name = f"{package_name}.{mod_name}"
        mod = importlib.import_module(full_name)
        yield from (
            obj
            for _, obj in inspect.getmembers(mod, inspect.isclass)
            if obj.__module__ == full_name
        )


def get_file_content(file_path: Path) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def build_container(config: Configuration) -> Container:
    container = Container()
    container.register(Configuration, instance=config)
    container.register(EntriesReducer)
    container.register(
        SteamApi,
        factory=lambda: SteamApi(config.get_steam_api_key(), config.get_steam_id()),
    )
    container.register(Store, factory=lambda: Store(config.get_database_path()))
    container.register(
        CommandBus, factory=lambda: CommandBus(container.resolve(Store), container)
    )
    container.register(HowLongToBeat)
    container.register(InputDataLoader)

    for command_class in get_classes_from("commands"):
        container.register(command_class)

    for query_class in get_classes_from("queries"):
        container.register(query_class)

    for presenter_class in get_classes_from("presenters"):
        container.register(presenter_class)

    return container


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s"
    )

    config = load_config()
    logging.info("Configuration loaded")

    container = build_container(config)
    store = container.resolve(Store)

    # Load games
    command_bus = container.resolve(CommandBus)
    input_data_loader = container.resolve(InputDataLoader).load()

import json
import logging
import importlib
import inspect
from pathlib import Path
import pkgutil
from typing import Generator
from commands.refresh_epic_games import RefreshEpicGamesCommand
from commands.refresh_gog_games import RefreshGogGamesCommand
from commands.refresh_steam_games import RefreshSteamGamesCommand
from presenters.to_csv import ToCsvPresenter
from queries.game_state_form import GameStateFormQuery
from services.command_bus import CommandBus
from services.config import Configuration, load_config
from services.entries_reducer import EntriesReducer
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

    command_bus.handle(RefreshSteamGamesCommand)
    command_bus.handle(
        RefreshGogGamesCommand,
        json.loads(get_file_content(Path("data/gog_games_20260105.json"))),
    )
    command_bus.handle(
        RefreshEpicGamesCommand,
        json.loads(get_file_content(Path("data/epic_games_20260109.json"))),
    )

    # Queries
    with open("form.csv", "w", encoding="utf-8") as file:
        container.resolve(ToCsvPresenter).present(
            container.resolve(GameStateFormQuery).execute(), file
        )

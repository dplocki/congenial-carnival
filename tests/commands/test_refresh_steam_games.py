from typing import Iterable
from unittest.mock import Mock

from models.entry import Entry
from models.event import AddSteamGameEvent, EventType, Event
from models.game_location import GameLocation
from commands.refresh_steam_games import RefreshSteamGamesCommand
from services.entries_reducer import EntriesReducer
from services.steam_api import SteamApi, SteamGameData
from tests.utils.data_providers import (
    build_entry_reducer,
    generate_entry,
    generate_int,
    generate_str,
)


def build_steam_game_entity(
    name: str, appid: int = None, rtime_last_played: int = None
) -> SteamGameData:
    return {
        "name": name,
        "appid": appid or str(generate_int()),
        "rtime_last_played": rtime_last_played or int(generate_int()),
    }


def build_steam_entry(**kwargs) -> Entry:
    kwargs["available"] = [GameLocation.STEAM]
    return generate_entry(**kwargs)


def execute_command(store: Mock, steam_api: Mock) -> Iterable[Event]:
    command = RefreshSteamGamesCommand(store, steam_api)
    return list(command.execute())


def execute_command(
    entries_reduce: EntriesReducer, steam_api: SteamApi
) -> Iterable[Event]:
    command = RefreshSteamGamesCommand(entries_reduce, steam_api)
    return list(command.execute())


def build_steam_api(*args) -> SteamApi:
    steam_api = Mock()
    steam_api.get_owned_games.return_value = args
    return steam_api


def test_execute_adds_new_steam_games():
    new_game_name = generate_str()
    new_game_api_id = generate_int()
    new_game_last_played = generate_int()
    entries_reduce = build_entry_reducer()
    steam_api = build_steam_api(
        build_steam_game_entity(new_game_name, new_game_api_id, new_game_last_played)
    )

    result = execute_command(entries_reduce, steam_api)

    assert len(result) == 1
    event = result[0]
    assert isinstance(event, AddSteamGameEvent)
    assert event.name == new_game_name
    assert event.api_id == new_game_api_id
    assert event.last_played == new_game_last_played


def test_execute_skips_already_owned():
    owned_game_title = generate_str()
    entries_reduce = build_entry_reducer(build_steam_game_entity(name=owned_game_title))
    steam_api = build_steam_api(build_steam_game_entity(owned_game_title))

    result = execute_command(entries_reduce, steam_api)

    assert len(result) == 0


def test_execute_detect_deleted_steam_games():
    owned_game_title = generate_str()
    entries_reduce = build_entry_reducer(build_steam_game_entity(name=owned_game_title))
    steam_api = build_steam_api()

    result = execute_command(entries_reduce, steam_api)

    assert len(result) == 1
    event = result[0]
    assert event.type == EventType.DELETE_GAME
    assert event.where_is == GameLocation.STEAM
    assert event.name == owned_game_title

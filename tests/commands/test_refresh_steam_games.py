from unittest.mock import Mock

from models.event import AddSteamGameEvent, EventType
from models.game_location import GameLocation
from commands.refresh_steam_games import RefreshSteamGamesCommand
from services.steam_api import SteamGameData
from tests.utils.data_providers import generate_int, generate_str


def build_add_steam_game_event(title: str) -> dict:
    return AddSteamGameEvent(title, api_id=generate_int(), last_played=generate_int())


def build_steam_game_entity(
    name: str, appid: int = None, rtime_last_played: int = None
) -> SteamGameData:
    return {
        "name": name,
        "appid": appid or str(generate_int()),
        "rtime_last_played": rtime_last_played or int(generate_int()),
    }


def test_execute_adds_new_steam_games():
    new_game_name = generate_str()
    new_game_api_id = generate_int()
    new_game_last_played = generate_int()

    steam_api = Mock()
    steam_api.get_owned_games.return_value = [
        build_steam_game_entity(new_game_name, new_game_api_id, new_game_last_played)
    ]

    store = Mock()
    store.get_all_events.return_value = []

    command = RefreshSteamGamesCommand(store, steam_api)
    command.execute()

    assert store.add_event.call_count == 1
    event = store.add_event.call_args[0][0]
    assert isinstance(event, AddSteamGameEvent)
    assert event.name == new_game_name
    assert event.api_id == new_game_api_id
    assert event.last_played == new_game_last_played


def test_execute_skips_already_owned():
    owned_game_title = generate_str()

    steam_api = Mock()
    steam_api.get_owned_games.return_value = [build_steam_game_entity(owned_game_title)]

    store = Mock()
    store.get_all_events.return_value = []

    cmd = RefreshSteamGamesCommand(store, steam_api)
    cmd.execute()

    assert store.add_game.call_count == 0


def test_execute_detect_deleted_steam_games():
    owned_game_title = generate_str()

    steam_api = Mock()
    steam_api.get_owned_games.return_value = []

    store = Mock()
    store.get_all_events.return_value = [build_add_steam_game_event(owned_game_title)]

    cmd = RefreshSteamGamesCommand(store, steam_api)
    cmd.execute()

    assert store.add_event.call_count == 1
    event = store.add_event.call_args[0][0]
    assert event.type == EventType.DELETE_GAME
    assert event.where_is == GameLocation.STEAM
    assert event.name == owned_game_title

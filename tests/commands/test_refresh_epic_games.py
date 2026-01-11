from unittest.mock import Mock

from src.commands.refresh_epic_games import RefreshEpicGamesCommand
from models.event import AddEpicGameEvent, DeleteGameEvent
from models.game_location import GameLocation
from tests.utils.data_providers import generate_str


def build_add_epic_game_event(name: str) -> AddEpicGameEvent:
    return AddEpicGameEvent(name=name)


def test_adds_new_epic_game_when_not_owned():
    new_game_name = generate_str()

    store = Mock()
    store.get_all_events.return_value = []

    command = RefreshEpicGamesCommand(store)
    command.execute([new_game_name])

    store.add_event.assert_called_once()

    event = store.add_event.call_args[0][0]
    assert isinstance(event, AddEpicGameEvent)
    assert event.name == new_game_name


def test_skips_existing_epic_game():
    owned_game_name = generate_str()

    store = Mock()
    store.get_all_events.return_value = [build_add_epic_game_event(owned_game_name)]

    command = RefreshEpicGamesCommand(store)
    command.execute([owned_game_name])

    store.add_event.assert_not_called()


def test_removes_epic_game_not_own_anymore():
    owned_game_name = generate_str()

    store = Mock()
    store.get_all_events.return_value = [
        build_add_epic_game_event(owned_game_name),
    ]

    command = RefreshEpicGamesCommand(store)
    command.execute([])

    store.add_event.assert_called()
    event = store.add_event.call_args[0][0]
    assert isinstance(event, DeleteGameEvent)
    assert event.name == owned_game_name and event.where_is == GameLocation.EPIC

from typing import Iterable
from unittest.mock import Mock

from src.commands.refresh_epic_games import RefreshEpicGamesCommand
from models.event import AddEpicGameEvent, DeleteGameEvent
from models.game_location import GameLocation
from models.event import Event
from tests.utils.data_providers import generate_str


def build_add_epic_game_event(name: str) -> AddEpicGameEvent:
    return AddEpicGameEvent(name=name)


def execute_command(store: Mock, games_titles: Iterable[str]) -> Iterable[Event]:
    command = RefreshEpicGamesCommand(store)
    return list(command.execute(games_titles))


def test_adds_new_epic_game_when_not_owned():
    new_game_name = generate_str()

    store = Mock()
    store.get_all_events.return_value = []

    event = execute_command(store, [new_game_name])[0]

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

    event = execute_command(store, [])[0]

    assert isinstance(event, DeleteGameEvent)
    assert event.name == owned_game_name and event.where_is == GameLocation.EPIC

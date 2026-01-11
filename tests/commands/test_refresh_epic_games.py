from unittest.mock import Mock

from src.commands.refresh_epic_games import RefreshEpicGamesCommand
from models.event import AddEpicGameEvent, DeleteGameEvent
from models.game_location import GameLocation
from tests.utils.data_providers import generate_str


def test_adds_new_epic_game_when_not_owned():
    new_game_name = generate_str()

    store = Mock()
    store.get_all_events.return_value = []

    cmd = RefreshEpicGamesCommand(store)
    cmd.execute([new_game_name])

    store.add_event.assert_called_once()
    store.remove_event.assert_not_called()

    event = store.add_event.call_args[0][0]
    assert isinstance(event, AddEpicGameEvent)
    assert event.name == new_game_name


def test_skips_existing_epic_game():
    owned_game_name = generate_str()

    store = Mock()
    store.get_all_events.return_value = [AddEpicGameEvent(name=owned_game_name)]

    cmd = RefreshEpicGamesCommand(store)
    cmd.execute([owned_game_name])

    store.add_event.assert_not_called()
    store.remove_event.assert_not_called()


def test_removes_epic_game_not_own_anymore():
    owned_game_name = generate_str()

    store = Mock()
    store.get_all_events.return_value = [AddEpicGameEvent(name=owned_game_name)]

    cmd = RefreshEpicGamesCommand(store)
    cmd.execute([])

    store.add_event.assert_called()
    event = store.add_event.call_args[0][0]
    assert isinstance(event, DeleteGameEvent)
    assert event.name == owned_game_name and event.where_is == GameLocation.EPIC

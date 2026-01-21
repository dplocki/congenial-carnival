from typing import Iterable
from unittest.mock import Mock
from src.commands.refresh_gog_games import GameData, RefreshGogGamesCommand
from models.event import AddGogGameEvent, MarkGameCompleteEvent, Event
from tests.utils.data_providers import generate_int, generate_str


def build_add_gog_game_event(title: str, gog_id: int = None) -> dict:
    return AddGogGameEvent(name=title, gog_id=gog_id or generate_int())


def build_mark_game_complete_event(title: str) -> dict:
    return MarkGameCompleteEvent(name=title)


def build_gog_game_entity(
    title: str, gog_id: int = None, is_complete: bool = False
) -> GameData:
    return {
        "title": title,
        "id": gog_id or generate_int(),
        "tags": ["COMPLETED"] if is_complete else [],
    }


def execute_command(store: Mock, games_data: Iterable[GameData]) -> Iterable[Event]:
    command = RefreshGogGamesCommand(store)
    return list(command.execute(games_data))


def test_adds_new_gog_game_when_not_owned():
    new_game_name = generate_str()
    new_game_id = generate_int()

    store = Mock()
    store.get_all_events.return_value = []

    event = execute_command(store, [build_gog_game_entity(new_game_name, new_game_id)])[
        0
    ]

    assert isinstance(event, AddGogGameEvent)
    assert event.name == new_game_name and event.gog_id == new_game_id


def test_skips_existing_gog_game():
    owned_game_name = generate_str()

    store = Mock()
    store.get_all_events.return_value = [build_add_gog_game_event(owned_game_name)]

    events = execute_command(store, [build_gog_game_entity(owned_game_name)])

    assert len(events) == 0


def test_marks_existing_game_complete():
    owned_game_name = generate_str()

    store = Mock()
    store.get_all_events.return_value = [
        build_add_gog_game_event(owned_game_name),
    ]

    event = execute_command(
        store, [build_gog_game_entity(owned_game_name, is_complete=True)]
    )[0]

    assert isinstance(event, MarkGameCompleteEvent) and event.name == owned_game_name


def test_does_not_mark_if_already_complete():
    owned_game_name = generate_str()

    store = Mock()
    store.get_all_events.return_value = [
        build_add_gog_game_event(owned_game_name),
        build_mark_game_complete_event(owned_game_name),
    ]

    cmd = RefreshGogGamesCommand(store)
    cmd.execute([build_gog_game_entity(owned_game_name, is_complete=True)])

    store.add_event.assert_not_called()

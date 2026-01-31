from typing import Iterable
from unittest.mock import Mock
from models.entry import Entry
from models.game_location import GameLocation
from services.entries_reducer import EntriesReducer
from src.commands.refresh_gog_games import GameData, RefreshGogGamesCommand
from models.event import AddGogGameEvent, MarkGameCompleteEvent, Event
from tests.utils.data_providers import (
    build_entry_reducer,
    generate_entry,
    generate_int,
    generate_str,
)


def build_gog_game_entity(
    title: str, gog_id: int = None, is_complete: bool = False
) -> GameData:
    return {
        "title": title,
        "id": gog_id or generate_int(),
        "tags": ["COMPLETED"] if is_complete else [],
    }


def build_gog_entry(**kwargs) -> Entry:
    kwargs["available"] = [GameLocation.GOG]
    return generate_entry(**kwargs)


def execute_command(
    entries_reduce: EntriesReducer, games_data: Iterable[GameData]
) -> Iterable[Event]:
    command = RefreshGogGamesCommand(entries_reduce)
    return list(command.execute(games_data))


def test_adds_new_gog_game_when_not_owned():
    new_game_name = generate_str()
    new_game_id = generate_int()
    entries_reduce = build_entry_reducer()

    result = execute_command(
        entries_reduce, [build_gog_game_entity(new_game_name, new_game_id)]
    )

    assert len(result) == 1
    event = result[0]
    assert isinstance(event, AddGogGameEvent)
    assert event.name == new_game_name and event.gog_id == new_game_id


def test_skips_existing_gog_game():
    owned_game_name = generate_str()
    entries_reduce = build_entry_reducer(build_gog_entry(name=owned_game_name))

    result = execute_command(entries_reduce, [build_gog_game_entity(owned_game_name)])

    assert len(result) == 0


def test_marks_existing_game_complete():
    owned_game_name = generate_str()
    entries_reduce = build_entry_reducer(build_gog_entry(name=owned_game_name))

    result = execute_command(
        entries_reduce, [build_gog_game_entity(owned_game_name, is_complete=True)]
    )

    assert len(result) == 1
    event = result[0]
    assert isinstance(event, MarkGameCompleteEvent) and event.name == owned_game_name


def test_does_not_mark_if_already_complete():
    owned_game_name = generate_str()
    entries_reduce = build_entry_reducer(
        build_gog_entry(name=owned_game_name, is_complete=True)
    )

    cmd = RefreshGogGamesCommand(entries_reduce)
    cmd.execute([build_gog_game_entity(owned_game_name, is_complete=True)])

    entries_reduce.add_event.assert_not_called()

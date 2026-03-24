from typing import Iterable
from unittest.mock import Mock

from models.entry import Entry
from models.event.type import EventType
from src.commands.refresh_epic_games import RefreshEpicGamesCommand
from models.game_location import GameLocation
from models.event import Event
from tests.utils.data_providers import build_entry_reducer, generate_entry, generate_str


def execute_command(
    entries_reducer: Mock, games_titles: Iterable[str]
) -> Iterable[Event]:
    command = RefreshEpicGamesCommand(entries_reducer)
    return list(command.execute(games_titles))


def build_epic_entry(**kwargs) -> Entry:
    kwargs["available"] = [GameLocation.EPIC]
    return generate_entry(**kwargs)


def test_adds_new_epic_game_when_not_owned():
    new_game_name = generate_str()
    entries_reducer = build_entry_reducer()

    event = execute_command(entries_reducer, [new_game_name])[0]

    assert event.type == EventType.ADD_GAME
    assert event.name == new_game_name
    assert event.where_is == GameLocation.EPIC


def test_skips_existing_epic_game():
    owned_game_name = generate_str()
    entries_reducer = build_entry_reducer(build_epic_entry(name=owned_game_name))

    result = execute_command(entries_reducer, [owned_game_name])

    assert len(result) == 0

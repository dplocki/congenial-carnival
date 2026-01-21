from pathlib import Path
from unittest.mock import Mock

from models.game_location import GameLocation
from src.commands.read_game_state_form import ReadGameStateFormCommand
from models.event import MarkGameCompleteEvent, MarkGameAsOtherEvent, RenameGameEvent
from tests.utils.data_providers import generate_enum, generate_str


def execute_command(csv_file_path: Path):
    command = ReadGameStateFormCommand()
    return list(command.execute(csv_file_path))


def test_marks_games_complete_for_yes_rows(tmp_path):
    file_name = generate_str()
    game_name = generate_str()
    csv_file_path = tmp_path / f"{file_name}.csv"
    csv_file_path.write_text(
        f"{game_name},{generate_enum(GameLocation)},yes,no,\n"
        f"{generate_str()},{generate_enum(GameLocation)},no,no,\n"
    )

    event = execute_command(csv_file_path)[0]

    assert isinstance(event, MarkGameCompleteEvent)
    assert event.name == game_name


def test_marks_games_as_other_for_not_a_game_yes(tmp_path):
    file_name = generate_str()
    game_name = generate_str()
    csv_file_path = tmp_path / f"{file_name}.csv"
    csv_file_path.write_text(
        f"{game_name},{generate_enum(GameLocation)},no,yes,\n"
        f"{generate_str()},{generate_enum(GameLocation)},no,no,\n"
    )

    event = execute_command(csv_file_path)[0]

    assert isinstance(event, MarkGameAsOtherEvent)
    assert event.name == game_name


def test_renames_games_for_different_game(tmp_path):
    file_name = generate_str()
    game_name = generate_str()
    new_game_name = generate_str()
    csv_file_path = tmp_path / f"{file_name}.csv"
    csv_file_path.write_text(
        f"{game_name},{generate_enum(GameLocation)},no,no,{new_game_name}\n"
        f"{generate_str()},{generate_enum(GameLocation)},no,no,\n"
    )

    event = execute_command(csv_file_path)[0]

    assert isinstance(event, RenameGameEvent)
    assert event.old_name == game_name
    assert event.new_name == new_game_name

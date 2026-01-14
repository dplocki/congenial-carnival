from unittest.mock import Mock

from models.game_location import GameLocation
from src.commands.read_game_state_form import ReadGameStateFormCommand
from models.event import MarkGameAsOtherEvent, MarkGameCompleteEvent
from tests.utils.data_providers import generate_enum, generate_str


def test_marks_games_complete_for_yes_rows(tmp_path):
    file_name = generate_str()
    game_name = generate_str()
    csv_file_path = tmp_path / f"{file_name}.csv"
    csv_file_path.write_text(
        f"{game_name},{generate_enum(GameLocation)},yes,no,no\n"
        f"{generate_str()},{generate_enum(GameLocation)},no,no,no\n"
    )

    store = Mock()

    command = ReadGameStateFormCommand(store)
    command.execute(csv_file_path)

    store.add_event.assert_called_once()
    event = store.add_event.call_args[0][0]

    assert isinstance(event, MarkGameCompleteEvent)
    assert event.name == game_name


def test_marks_games_as_other_for_yes_rows(tmp_path):
    file_name = generate_str()
    game_name = generate_str()
    csv_file_path = tmp_path / f"{file_name}.csv"
    csv_file_path.write_text(
        f"{game_name},{generate_enum(GameLocation)},no,yes,no\n"
        f"{generate_str()},{generate_enum(GameLocation)},no,no,no\n"
    )

    store = Mock()

    command = ReadGameStateFormCommand(store)
    command.execute(csv_file_path)

    store.add_event.assert_called_once()
    event = store.add_event.call_args[0][0]

    assert isinstance(event, MarkGameAsOtherEvent)
    assert event.name == game_name

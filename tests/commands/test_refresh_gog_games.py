from unittest.mock import Mock
from src.commands.refresh_gog_games import RefreshGogGamesCommand
from models.event import AddGogGameEvent, MarkGameCompleteEvent
from models.game_location import GameLocation
from tests.utils.data_providers import generate_game, generate_int, generate_str


def test_adds_new_gog_game_when_not_owned():
    new_game_name = generate_str()
    new_game_id = generate_int()

    games = Mock()
    games.get_all_games.return_value = []
    games.get_game.return_value = generate_game(
        name=new_game_name, available={GameLocation.GOG}
    )

    cmd = RefreshGogGamesCommand(config=Mock(), games=games)
    cmd.execute([{"title": new_game_name, "id": new_game_id, "tags": []}])

    games.add_game.assert_called_once()
    games.change_game_state.assert_not_called()
    games.remove_game.assert_not_called()

    event = games.add_game.call_args[0][0]
    assert isinstance(event, AddGogGameEvent)
    assert event.name == new_game_name and event.gog_id == new_game_id


def test_skips_existing_gog_game():
    owned_game_name = generate_str()
    owned_game = generate_game(name=owned_game_name, available={GameLocation.GOG})

    games = Mock()
    games.get_all_games.return_value = [owned_game]
    games.get_game.return_value = owned_game

    cmd = RefreshGogGamesCommand(config=Mock(), games=games)
    cmd.execute([{"title": owned_game_name, "id": generate_int(), "tags": []}])

    games.add_game.assert_not_called()
    games.change_game_state.assert_not_called()
    games.remove_game.assert_not_called()


def test_marks_existing_game_complete():
    owned_game_name = generate_str()
    owned_game = generate_game(name=owned_game_name, available={GameLocation.GOG})

    games = Mock()
    games.get_all_games.return_value = [owned_game]
    games.get_game.return_value = owned_game

    cmd = RefreshGogGamesCommand(config=Mock(), games=games)
    cmd.execute(
        [{"title": owned_game_name, "id": generate_int(), "tags": ["COMPLETED"]}]
    )

    games.change_game_state.assert_called_once()
    evt = games.change_game_state.call_args[0][0]
    assert isinstance(evt, MarkGameCompleteEvent) and evt.name == owned_game_name


def test_does_not_mark_if_already_complete():
    owned_game_name = generate_str()
    owned_game = generate_game(
        name=owned_game_name, available={GameLocation.GOG}, is_complete=True
    )

    games = Mock()
    games.get_all_games.return_value = [owned_game]
    games.get_game.return_value = owned_game

    cmd = RefreshGogGamesCommand(config=Mock(), games=games)
    cmd.execute([{"title": owned_game_name, "id": generate_int(), "tags": ["COMPLETED"]}])

    games.change_game_state.assert_not_called()

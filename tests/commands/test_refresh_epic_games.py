from unittest.mock import Mock

from src.commands.refresh_epic_games import RefreshEpicGamesCommand
from models.event import AddEpicGameEvent, DeleteGameEvent
from models.game_location import GameLocation
from tests.utils.data_providers import generate_game, generate_str


def test_adds_new_epic_game_when_not_owned():
    new_game_name = generate_str()

    games = Mock()
    games.get_all_games.return_value = []

    cmd = RefreshEpicGamesCommand(games=games)
    cmd.execute([new_game_name])

    games.add_game.assert_called_once()
    games.remove_game.assert_not_called()

    event = games.add_game.call_args[0][0]
    assert isinstance(event, AddEpicGameEvent)
    assert event.name == new_game_name


def test_skips_existing_epic_game():
    owned_game_name = generate_str()
    owned_game = generate_game(name=owned_game_name, available={GameLocation.EPIC})

    games = Mock()
    games.get_all_games.return_value = [owned_game]
    games.get_game.return_value = owned_game

    cmd = RefreshEpicGamesCommand(games=games)
    cmd.execute([owned_game_name])

    games.add_game.assert_not_called()
    games.remove_game.assert_not_called()


def test_removes_epic_game_not_own_anymore():
    owned_game_name = generate_str()
    owned_game = generate_game(name=owned_game_name, available={GameLocation.EPIC})

    games = Mock()
    games.get_all_games.return_value = [owned_game]

    cmd = RefreshEpicGamesCommand(games=games)
    cmd.execute([])

    games.remove_game.assert_called_once()
    event = games.remove_game.call_args[0][0]
    assert isinstance(event, DeleteGameEvent)
    assert event.name == owned_game_name and event.where_is == GameLocation.EPIC

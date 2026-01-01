from unittest.mock import Mock

from models.event import AddSteamGameEvent
from models.game import Game
from models.game_location import GameLocation
from commands.refresh_steam_games import RefreshSteamGamesCommand
from tests.utils.data_providers import generate_game, generate_int, generate_str


def test_execute_adds_new_steam_games():
    games = Mock()
    games.get_all_games.return_value = [generate_game(available=[GameLocation.OTHER])]
    games.add_game = Mock()

    new_game_name = generate_str()
    new_game_api_id = str(generate_int())
    new_game_last_played = generate_int()
    steam_api = Mock()
    steam_api.get_owned_games.return_value = [
        {
            "name": new_game_name,
            "appid": new_game_api_id,
            "rtime_last_played": new_game_last_played,
        }
    ]

    command = RefreshSteamGamesCommand(games, steam_api)
    command.execute()

    assert games.add_game.call_count == 1
    added_event = games.add_game.call_args[0][0]
    assert isinstance(added_event, AddSteamGameEvent)
    assert added_event.name == new_game_name
    assert added_event.api_id == new_game_api_id
    assert added_event.last_played == new_game_last_played


def test_execute_skips_already_owned_and_logs_missing():
    owned_game_title = generate_str()

    games = Mock()
    games.get_all_games.return_value = [
        generate_game(name=owned_game_title, available=[GameLocation.STEAM])
    ]
    games.add_game = Mock()

    steam_api = Mock()
    steam_api.get_owned_games.return_value = [
        {
            "name": owned_game_title,
            "appid": str(generate_int()),
            "rtime_last_played": 111,
        }
    ]

    cmd = RefreshSteamGamesCommand(games, steam_api)
    cmd.execute()

    assert games.add_game.call_count == 0


def test_execute_detect_deleted_steam_games():
    owned_game_title = generate_str()
    owned_game_api_id = str(generate_int())

    games = Mock()
    games.get_all_games.return_value = [
        generate_game(
            name=owned_game_title,
            api_id=owned_game_api_id,
            available=[GameLocation.STEAM],
        )
    ]
    games.remove_game = Mock()

    steam_api = Mock()
    steam_api.get_owned_games.return_value = []

    cmd = RefreshSteamGamesCommand(games, steam_api)
    cmd.execute()

    assert games.remove_game.call_count == 1
    removed_game = games.remove_game.call_args[0][0]
    assert removed_game.name == owned_game_title

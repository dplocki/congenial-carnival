import pytest
from unittest.mock import Mock
from src.commands.refresh_gog_games import RefreshGogGamesCommand
from models.event import AddGogGameEvent, DeleteGogGameEvent, MarkGameCompleteEvent
from models.game_location import GameLocation
from tests.utils.data_providers import generate_int, generate_str


class GameStub:
    def __init__(self, name, id_complete=False, available=None):
        self.name = name
        self.id_complete = id_complete
        self.available = available or set()


def test_adds_new_gog_game_when_not_owned():
    new_game_name = generate_str()
    new_game_id = generate_int()

    games = Mock()
    games.get_all_games.return_value = []
    games.get_game.return_value = GameStub(
        new_game_name, id_complete=False, available={GameLocation.GOG}
    )

    cmd = RefreshGogGamesCommand(config=Mock(), games=games)
    cmd.execute([{"title": new_game_name, "id": new_game_id, "tags": []}])

    games.add_game.assert_called_once()
    games.change_game_state.assert_not_called()
    games.remove_game.assert_not_called()

    event = games.add_game.call_args[0][0]
    assert isinstance(event, AddGogGameEvent)
    assert event.name == new_game_name and event.gog_id == new_game_id

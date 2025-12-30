from unittest.mock import Mock

from models.game_location import GameLocation
from services.games import Games
from tests.utils.asserts import are_collections_equal
from tests.utils.data_providers import generate_str


def test_get_all_games_empty():
    store = Mock()
    store.get_all_events.return_value = []

    games_service = Games(store)

    first_time_all_games = list(games_service.get_all_games())
    second_time_all_games = list(games_service.get_all_games())

    assert first_time_all_games == []
    assert store.get_all_events.call_count == 1
    assert are_collections_equal(first_time_all_games, second_time_all_games)


def test_get_all_games_aggregates_events():
    store = Mock()
    single_game_title = generate_str()
    repeating_game_title = generate_str()
    store.get_all_events.return_value = [
        {"name": repeating_game_title, "where_is": GameLocation.STEAM},
        {"name": single_game_title, "where_is": GameLocation.OTHER},
        {"name": repeating_game_title, "where_is": GameLocation.GOG},
    ]

    games_service = Games(store)
    all_games = list(games_service.get_all_games())

    assert len(all_games) == 2

    game_from_two_sources = next(g for g in all_games if g.name == repeating_game_title)
    assert GameLocation.STEAM in game_from_two_sources.available
    assert GameLocation.GOG in game_from_two_sources.available

    game_from_single_sources = next(g for g in all_games if g.name == single_game_title)
    assert game_from_single_sources.available == [GameLocation.OTHER]

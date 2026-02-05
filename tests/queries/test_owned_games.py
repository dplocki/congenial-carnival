from models.game_location import GameLocation
from queries.owned_games import OwnedGamesQuery
from services.entries_reducer import EntriesReducer
from tests.utils.data_providers import (
    build_entry_reducer,
    generate_entry,
    generate_enum,
    generate_str,
)


def execute_query(entries_reducer: EntriesReducer) -> OwnedGamesQuery:
    query = OwnedGamesQuery(entries_reducer)

    return list(query.execute())


def build_owned_games_data(
    name: str = None,
    available: GameLocation = None,
    is_game: bool = None,
    is_complete: bool = None,
) -> dict:
    return {
        "name": name or generate_str(),
        "available": available or generate_enum(GameLocation),
        "is_game": is_game or True,
        "is_complete": is_complete or False,
    }


def test_query_should_return_owned_games():
    game_name_1 = generate_str()
    available = generate_enum(GameLocation)

    reducer_mock = build_entry_reducer(
        generate_entry(
            name=game_name_1,
            available={available},
            is_game=True,
        )
    )

    results = execute_query(reducer_mock)

    assert results[0]["name"] == game_name_1
    assert results[0]["platforms"] == available
    assert results[0]["is_complete"] is False


def test_query_should_return_sorted_owned_games():
    game_name_1 = "Z" + generate_str()
    game_name_2 = "A" + generate_str()

    reducer_mock = build_entry_reducer(
        generate_entry(
            name=game_name_1,
            is_game=True,
            is_complete=False,
        ),
        generate_entry(
            name=game_name_2,
            is_game=True,
            is_complete=True,
        ),
    )

    results = execute_query(reducer_mock)

    assert results[0]["name"] == game_name_2
    assert results[1]["name"] == game_name_1


def test_query_should_filter_non_games():
    game_name_1 = generate_str()
    game_name_2 = generate_str()

    reducer_mock = build_entry_reducer(
        generate_entry(
            name=game_name_1,
            is_game=True,
        ),
        generate_entry(
            name=game_name_2,
            is_game=False,
        ),
    )

    results = execute_query(reducer_mock)

    assert len(results) == 1
    assert results[0]["name"] == game_name_1

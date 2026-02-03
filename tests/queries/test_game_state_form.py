from typing import Iterable
from models.game_location import GameLocation
from queries.game_state_form import GameStateFormQuery
from services.entries_reducer import EntriesReducer
from tests.utils.data_providers import (
    build_entry_reducer,
    generate_entry,
    generate_enum,
    generate_str,
)


def execute_query(entries_reducer: EntriesReducer) -> Iterable[GameStateFormQuery]:
    return list(GameStateFormQuery(entries_reducer).execute())


def test_should_return_games():
    game_name_1 = generate_str()
    game_location_1 = generate_enum(GameLocation)
    game_is_complete_1 = True
    reducer_mock = build_entry_reducer(
        generate_entry(
            name=game_name_1,
            available={game_location_1},
            is_complete=game_is_complete_1,
        )
    )

    result = execute_query(reducer_mock)

    assert len(result) == 1

    assert result[0]["name"] == game_name_1
    assert result[0]["platforms"] == game_location_1
    assert result[0]["is_complete"] is game_is_complete_1
    assert result[0]["is_not_a_game"] is False
    assert result[0]["is_different_game"] is False

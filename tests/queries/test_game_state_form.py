from typing import Iterable
from queries.game_state_form import GameStateFormQuery
from services.entries_reducer import EntriesReducer
from tests.utils.data_providers import build_entry_reducer, generate_entry, generate_str


def execute_query(entries_reducer: EntriesReducer) -> Iterable[GameStateFormQuery]:
    return list(GameStateFormQuery(entries_reducer).execute())


def test_should_return_games():
    game_name_1 = generate_str()
    reducer_mock = build_entry_reducer(generate_entry(name=game_name_1))

    result = execute_query(reducer_mock)

    assert len(result) == 1
    assert result[0]["name"] == game_name_1

from typing import Generator, TypedDict
from services.entries_reducer import EntriesReducer


class GameStateFormData(TypedDict):
    name: str
    platforms: str
    is_complete: bool
    is_not_a_game: bool
    different_game: str


class GameStateFormQuery:
    def __init__(self, entries_reducer: EntriesReducer):
        self.entries_reducer = entries_reducer

    def execute(self) -> Generator[GameStateFormData, None, None]:
        only_games = filter(lambda entry: entry.is_game, self.entries_reducer.get_all_entries())

        for entry in sorted(only_games, key=lambda entry: entry.name):
            yield GameStateFormData(
                name=entry.name,
                platforms=" ".join(entry.available),
                is_complete=entry.is_complete,
                is_not_a_game=not entry.is_game,
                different_game="",
            )

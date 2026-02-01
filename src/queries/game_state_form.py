from typing import Generator, TypedDict
from services.entries_reducer import EntriesReducer


class GameStateFormData(TypedDict):
    name: str
    platforms: str
    is_complete: bool
    is_not_a_game: bool
    is_different_game: bool


class GameStateFormQuery:
    def __init__(self, entries_reducer: EntriesReducer):
        self.entries_reducer = entries_reducer

    def execute(self) -> Generator[GameStateFormData, None, None]:
        for entry in self.entries_reducer.get_all_entries():
            if not entry.is_game:
                continue

            yield GameStateFormData(
                name=entry.name,
                platforms=" ".join(entry.available),
                is_complete=entry.is_complete,
                is_not_a_game=False,
                is_different_game=False,
            )

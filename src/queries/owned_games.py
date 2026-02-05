from typing import TypedDict
from services.entries_reducer import EntriesReducer


class OwnedGamesData(TypedDict):
    name: str
    is_complete: bool
    platforms: str


class OwnedGamesQuery:

    def __init__(self, games_reducer: EntriesReducer):
        self.games_reducer = games_reducer

    def execute(self):
        return sorted(
            (
                OwnedGamesData(
                    name=entry.name,
                    is_complete=entry.is_complete,
                    platforms=" ".join(entry.available),
                )
                for entry in self.games_reducer.get_all_entries()
                if entry.is_game
            ),
            key=lambda game: game["name"].lower(),
        )

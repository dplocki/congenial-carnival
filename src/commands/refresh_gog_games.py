import logging
from typing import Generator, Iterable, TypedDict
from models.event import (
    AddGogGameEvent,
    DeleteGogGameEvent,
    MarkGameCompleteEvent,
)
from models.game_location import GameLocation
from models.event import Event
from services.entries_reducer import EntriesReducer


logger = logging.getLogger(__name__)
COMPLETED_TAG = "COMPLETED"


class GameData(TypedDict):
    title: str
    id: int
    tags: Iterable[str]


class RefreshGogGamesCommand:
    def __init__(self, reducer: EntriesReducer):
        self.reducer: EntriesReducer = reducer

    def execute(self, games_data: Iterable[GameData]) -> Generator[Event, None, None]:
        already_own_gog_games = set()
        completed_games = set()

        for entry in self.reducer.get_all_entries():
            if not entry.is_game:
                continue

            if GameLocation.GOG not in entry.available:
                continue

            already_own_gog_games.update(entry.all_names)

            if entry.is_complete:
                completed_games.update(entry.all_names)

        for game_datum in games_data:
            title = game_datum["title"].strip()
            if title not in already_own_gog_games:
                logger.info(f"Adding new game on Gog: {title}")
                yield AddGogGameEvent(title, game_datum["id"])
            else:
                already_own_gog_games.remove(title)

            if title not in completed_games and COMPLETED_TAG in game_datum["tags"]:
                logger.info(f"Game complete: {title} (Gog)")
                yield MarkGameCompleteEvent(title)

        for game_name in already_own_gog_games:
            logger.info(f"Removing game from Gog: {game_name}")
            yield DeleteGogGameEvent(game_name)

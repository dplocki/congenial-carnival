import logging
from models.event import Event
from typing import Generator, Iterable
from models.event import AddEpicGameEvent, DeleteGameEvent, EventType
from models.game_location import GameLocation
from services.entries_reducer import EntriesReducer


logger = logging.getLogger(__name__)


class RefreshEpicGamesCommand:
    def __init__(self, entries_reducer: EntriesReducer):
        self.store = entries_reducer

    def execute(self, games_titles: Iterable[str]) -> Generator[Event, None, None]:
        existing_titles = set()
        for entry in self.store.get_all_entries():
            if GameLocation.EPIC not in entry.available:
                continue

            existing_titles.add(entry.name)
            existing_titles.update(entry.aliases)

        for title in set(games_titles) ^ existing_titles:
            logger.info(f"Adding new game on Epic: {title}")
            yield AddEpicGameEvent(title)

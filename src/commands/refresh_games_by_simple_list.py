from datetime import datetime
import logging
from typing import Generator, Iterable
from models.event import Event

from models.event.add_game import AddGameEvent
from models.game_location import GameLocation
from services.entries_reducer import EntriesReducer


logger = logging.getLogger(__name__)


class RefreshGamesBySimpleListCommand:

    def __init__(self, game_type: GameLocation, entries_reducer: EntriesReducer):
        self.game_type = game_type
        self.entries_reducer = entries_reducer

    def execute(
        self, games_titles: Iterable[str], file_time: datetime = None
    ) -> Generator[Event, None, None]:
        existing_titles = set()
        for entry in self.entries_reducer.get_all_entries():
            if self.game_type not in entry.available:
                continue

            existing_titles.update(entry.all_names)

        for title in set(games_titles) - existing_titles:
            logger.info(f"Adding new game on {self.game_type}: {title}")
            yield AddGameEvent(title, self.game_type, timestamp=file_time)

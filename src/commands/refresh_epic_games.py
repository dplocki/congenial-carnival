import logging
from models.event import Event
from typing import Generator, Iterable
from models.event import AddEpicGameEvent, DeleteGameEvent, EventType
from models.game_location import GameLocation
from services.store import Store


logger = logging.getLogger(__name__)


class RefreshEpicGamesCommand:
    def __init__(self, store: Store):
        self.store = store

    def execute(self, games_titles: Iterable[str]) -> Generator[Event, None, None]:
        existing_titles = set(
            event.name
            for event in self.store.get_all_events()
            if event.type == EventType.ADD_GAME and event.where_is == GameLocation.EPIC
        )

        for title in set(games_titles) ^ existing_titles:
            if title in existing_titles:
                logger.info(f"Removing game from Epic: {title}")
                yield DeleteGameEvent(title, GameLocation.EPIC)
            else:
                logger.info(f"Adding new game on Epic: {title}")
                yield AddEpicGameEvent(title)

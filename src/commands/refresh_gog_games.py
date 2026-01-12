import logging
from operator import attrgetter
from typing import Iterable, TypedDict
from models.event import (
    AddGogGameEvent,
    DeleteGogGameEvent,
    EventType,
    MarkGameCompleteEvent,
)
from models.game_location import GameLocation
from services.store import Store


logger = logging.getLogger(__name__)
COMPLETED_TAG = "COMPLETED"


class GameData(TypedDict):
    title: str
    id: int
    tags: Iterable[str]


class RefreshGogGamesCommand:
    def __init__(self, store: Store):
        self.store: Store = store

    def execute(self, games_data: Iterable[GameData]) -> None:
        already_own_gog_games = set()
        completed_games = set()

        for event in self.store.get_all_events():
            if event.type == EventType.ADD_GAME and event.where_is == GameLocation.GOG:
                already_own_gog_games.add(event.name)
            elif event.type == EventType.COMPLETED_GAME:
                completed_games.add(event.name)

        for game_datum in games_data:
            title = game_datum["title"].strip()
            if title not in already_own_gog_games:
                logger.info(f"Adding new game on Gog: {title}")
                self.store.add_event(AddGogGameEvent(title, game_datum["id"]))
            else:
                already_own_gog_games.remove(title)

            if title not in completed_games and COMPLETED_TAG in game_datum["tags"]:
                logger.info(f"Game complete: {title} (Gog)")
                self.store.add_event(MarkGameCompleteEvent(title))

        for game_name in already_own_gog_games:
            logger.info(f"Removing game from Gog: {game_name}")
            self.store.add_event(DeleteGogGameEvent(game_name))

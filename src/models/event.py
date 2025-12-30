from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum

from models.game_location import GameLocation


class EventType(StrEnum):
    ADD_GAME = "add_game"


@dataclass(frozen=True, init=False)
class Event:
    type: EventType
    timestamp: int

    def __init__(self, type: EventType, timestamp: int = None):
        object.__setattr__(self, "type", type)
        object.__setattr__(
            self, "timestamp", timestamp or int(datetime.now(timezone.utc).timestamp())
        )


@dataclass(frozen=True, init=False)
class AddGameEvent(Event):
    name: str
    where_is: GameLocation

    def __init__(self, name: str, where_is: GameLocation, timestamp: int = None):
        super().__init__(EventType.ADD_GAME, timestamp)
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "where_is", where_is)


@dataclass(frozen=True, init=False)
class AddSteamGameEvent(AddGameEvent):
    api_id: str
    last_played: int

    def __init__(
        self, name: str, api_id: str, last_played: int = None, timestamp: int = None
    ):
        super().__init__(name, GameLocation.STEAM, timestamp)
        object.__setattr__(self, "api_id", api_id)
        object.__setattr__(self, "last_played", last_played)

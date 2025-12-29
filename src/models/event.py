from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import ClassVar


class EventType(StrEnum):
    ADD_GAME = "add_game"


class GameLocation(StrEnum):
    STEAM = "steam"
    GOG = "gog"
    EPIC = "epic"
    OTHER = "other"


@dataclass(frozen=True)
class Event:
    type: EventType
    timestamp: datetime

    def __init__(self, type: EventType, timestamp: datetime = None):
        object.__setattr__(self, "type", type)
        object.__setattr__(
            self,
            "timestamp",
            datetime.now(timezone.utc) if timestamp is None else timestamp,
        )


@dataclass(frozen=True)
class AddGameEvent(Event):
    where_is: GameLocation

    def __init__(self, where_is: GameLocation, timestamp: datetime = None):
        super().__init__(EventType.ADD_GAME, timestamp)
        object.__setattr__(self, "where_is", where_is)


@dataclass(frozen=True)
class AddSteamGameEvent(AddGameEvent):
    api_id: str

    def __init__(self, api_id: str, timestamp: datetime = None):
        super().__init__(GameLocation.STEAM, timestamp)
        object.__setattr__(self, "api_id", api_id)

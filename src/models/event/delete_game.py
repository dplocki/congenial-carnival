from dataclasses import dataclass
from .event import Event
from models.event.type import EventType
from models.game_location import GameLocation


@dataclass(frozen=True, init=False)
class DeleteGameEvent(Event):
    name: str
    where_is: GameLocation

    def __init__(self, name: str, where_is: GameLocation, timestamp: int = None):
        super().__init__(EventType.DELETE_GAME, timestamp)
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "where_is", where_is)


@dataclass(frozen=True, init=False)
class DeleteSteamGameEvent(DeleteGameEvent):
    name: str

    def __init__(self, name: str, timestamp: int = None):
        super().__init__(name, GameLocation.STEAM, timestamp)


@dataclass(frozen=True, init=False)
class DeleteGogGameEvent(DeleteGameEvent):
    name: str

    def __init__(self, name: str, timestamp: int = None):
        super().__init__(name, GameLocation.GOG, timestamp)

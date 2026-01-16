from dataclasses import dataclass
from .event import Event
from models.event.type import EventType
from models.game_location import GameLocation


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


@dataclass(frozen=True, init=False)
class AddGogGameEvent(AddGameEvent):
    gog_id: int

    def __init__(self, name: str, gog_id: int, timestamp: int = None):
        super().__init__(name, GameLocation.GOG, timestamp)
        object.__setattr__(self, "gog_id", gog_id)


@dataclass(frozen=True, init=False)
class AddEpicGameEvent(AddGameEvent):
    def __init__(self, name: str, timestamp: int = None):
        super().__init__(name, GameLocation.EPIC, timestamp)

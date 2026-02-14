from dataclasses import dataclass
from .event import Event
from models.event import EventType


@dataclass(frozen=True, init=False)
class MarkGameCompleteEvent(Event):
    name: str

    def __init__(self, name: str, timestamp: int = None):
        super().__init__(EventType.COMPLETED_GAME, timestamp)
        object.__setattr__(self, "name", name)


@dataclass(frozen=True, init=False)
class MarkGameAsOtherEvent(Event):
    name: str

    def __init__(self, name: str, timestamp: int = None):
        super().__init__(EventType.MARK_AS_NOT_GAME, timestamp)
        object.__setattr__(self, "name", name)


@dataclass(frozen=True, init=False)
class RenameGameEvent(Event):
    old_name: str
    new_name: str

    def __init__(self, old_name: str, new_name: str, timestamp: int = None):
        super().__init__(EventType.RENAME_GAME, timestamp)
        object.__setattr__(self, "old_name", old_name)
        object.__setattr__(self, "new_name", new_name)


@dataclass(frozen=True, init=False)
class AddGameCompletionTimeEvent(Event):
    game_name: str
    time_to_complete: float

    def __init__(self, game_name: str, time_to_complete: float, timestamp: int = None):
        super().__init__(EventType.ADD_COMPLETION_TIME, timestamp)
        object.__setattr__(self, "game_name", game_name)
        object.__setattr__(self, "time_to_complete", time_to_complete)

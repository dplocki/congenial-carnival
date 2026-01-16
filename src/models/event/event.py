from dataclasses import dataclass
from datetime import datetime, timezone
from models.event.type import EventType


@dataclass(frozen=True, init=False)
class Event:
    type: EventType
    timestamp: int

    def __init__(self, type: EventType, timestamp: int = None):
        object.__setattr__(self, "type", type)
        object.__setattr__(
            self, "timestamp", timestamp or int(datetime.now(timezone.utc).timestamp())
        )

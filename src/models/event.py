from dataclasses import dataclass
import datetime
from enum import StrEnum


class EventType(StrEnum):
    ADD_GAME = "add_game"


@dataclass(frozen=True)
class Event[T = str]:
    type: EventType
    timestamp: datetime = datetime.now()
    data: T

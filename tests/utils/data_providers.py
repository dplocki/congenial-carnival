from enum import Enum
import random
import string
from typing import Type

from models.event import AddGameEvent, Event
from models.game_location import GameLocation


def generate_str(length: int = 10) -> str:
    """Generate a random string of fixed length."""
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def generate_enum[E: Enum](enum_type: type[E]) -> E:
    """Generate a random value from the specified enum type."""
    return random.choice(list(enum_type))


def generate_event(event_type: Type, **kwargs) -> Event:
    """Generate a random event of the specified type."""
    if event_type == AddGameEvent:
        name = kwargs.get("name", generate_str())
        where_is = kwargs.get("where_is", generate_enum(GameLocation))
        timestamp = kwargs.get("timestamp", random.randint(1, 1_000_000))
        return AddGameEvent(name, where_is, timestamp)

    raise ValueError(f"Unsupported event type: {event_type}")

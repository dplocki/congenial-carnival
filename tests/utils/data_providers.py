from enum import Enum
import random
import string
from typing import Type

from models.event import AddGameEvent, Event
from models.game import Game
from models.game_location import GameLocation


def generate_str(length: int = 10) -> str:
    """Generate a random string of fixed length."""
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def generate_int(start: int = 1000, end: int = 9999) -> int:
    """Generate a random integer within the specified range."""
    return random.randint(start, end)


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


def generate_game(**kwargs) -> Game:
    """Generate a Game instance with random or specified attributes."""
    name = kwargs.get("name", generate_str())
    available = kwargs.get("available", [])
    is_complete = kwargs.get("is_complete", False)

    return Game(name=name, available=available, is_complete=is_complete)

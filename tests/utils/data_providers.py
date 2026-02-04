from enum import Enum
import random
import string
from typing import Type
from unittest.mock import Mock
import inspect

from models.event import Event
from models.entry import Entry
from models.game_location import GameLocation
from models.note_type import NoteType
from services.entries_reducer import EntriesReducer


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
    sig = inspect.signature(event_type.__init__)
    init_kwargs = {}

    for param_name, param in sig.parameters.items():
        if param_name == "self" or param_name == "timestamp":
            continue

        if param_name in kwargs:
            init_kwargs[param_name] = kwargs[param_name]
        elif param.default is inspect.Parameter.empty:
            if param_name in (
                "name",
                "game_name",
                "old_name",
                "new_name",
                "different_game",
            ):
                init_kwargs[param_name] = generate_str()
            elif param_name in ("api_id",):
                init_kwargs[param_name] = str(generate_int())
            elif param_name in ("gog_id", "last_played"):
                init_kwargs[param_name] = generate_int()
            elif param_name in ("where_is",):
                init_kwargs[param_name] = generate_enum(GameLocation)
            elif param_name in ("note_type",):
                init_kwargs[param_name] = generate_enum(NoteType)
            else:
                init_kwargs[param_name] = generate_str()

    if "timestamp" in kwargs:
        init_kwargs["timestamp"] = kwargs["timestamp"]

    return event_type(**init_kwargs)


def generate_entry(**kwargs) -> Entry:
    """Generate a Game instance with random or specified attributes."""
    name = kwargs.get("name", generate_str())
    available = kwargs.get("available", set())
    if len(available) == 0:
        available.add(generate_enum(GameLocation))

    is_complete = kwargs.get("is_complete", False)
    all_names = kwargs.get("all_names", set())
    all_names.add(name)

    return Entry(
        name=name, available=available, is_complete=is_complete, all_names=all_names
    )


def build_entry_reducer(*args: Entry) -> EntriesReducer:
    entries_reducer = Mock()
    entries_reducer.get_all_entries.return_value = args
    return entries_reducer

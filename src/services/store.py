from typing import Iterable, List
from tinydb import TinyDB

from models.event import (
    AddEpicGameEvent,
    AddGameEvent,
    AddGogGameEvent,
    AddSteamGameEvent,
    DeleteGameEvent,
    Event,
    EventType,
    MarkGameCompleteEvent,
)
from models.game_location import GameLocation


class Store:
    def __init__(self, db_file_path: str):
        self.db = TinyDB(db_file_path)
        self.events = None
        self.table_events = self.db.table("events")

    def add_event(self, event: AddGameEvent):
        self.table_events.insert(event.__dict__)

    def get_all_events(self) -> Iterable[Event]:
        if self.events is None:
            self.events = list(map(parse_event, self.table_events.all()))

        return self.events


def parse_event(data: dict):
    event_type: EventType = data.get("type", None)
    del data["type"]

    if event_type == EventType.ADD_GAME:
        game_location = data.get("where_is")
        del data["where_is"]

        if game_location == GameLocation.STEAM:
            return AddSteamGameEvent(**data)
        elif game_location == GameLocation.GOG:
            return AddGogGameEvent(**data)
        elif game_location == GameLocation.EPIC:
            return AddEpicGameEvent(**data)

        raise ValueError(f"Unknown add game type: {event_type}")

    elif event_type == EventType.DELETE_GAME:
        return DeleteGameEvent(**data)
    elif event_type == EventType.COMPLETED_GAME:
        return MarkGameCompleteEvent(**data)

    raise ValueError(f"Unknown event type: {event_type}")

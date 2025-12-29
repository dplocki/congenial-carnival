from typing import List
from tinydb import TinyDB

from models.event import AddGameEvent


class Store:
    def __init__(self, db_file_path: str):
        self.db = TinyDB(db_file_path)
        self.events = self.db.table("events")

    def add_event(self, event: AddGameEvent):
        self.events.insert(event.__dict__)

    def get_all_events(self) -> List:
        return self.events.all()

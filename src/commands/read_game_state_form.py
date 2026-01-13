import csv
from pathlib import Path
from models.event import MarkGameCompleteEvent
from services.store import Store


class ReadGameStateFormCommand:
    def __init__(self, store: Store):
        self.store = store

    def execute(self, csv_file_path: Path):
        with open(csv_file_path) as csv_file:
            for name, _, complete, not_a_game, different_game in csv.reader(csv_file):
                if complete.lower() == "yes":
                    self.store.add_event(MarkGameCompleteEvent(name))

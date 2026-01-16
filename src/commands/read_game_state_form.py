import csv
import logging
from pathlib import Path
from models.event import MarkGameCompleteEvent, MarkGameAsOtherEvent, RenameGameEvent
from services.store import Store


logger = logging.getLogger(__name__)


class ReadGameStateFormCommand:
    def __init__(self, store: Store):
        self.store = store

    def execute(self, csv_file_path: Path):
        with open(csv_file_path) as csv_file:
            for name, _, complete, not_a_game, different_game in csv.reader(csv_file):
                if complete.lower() == "yes":
                    logger.info(f"Marking game complete: {name}")
                    self.store.add_event(MarkGameCompleteEvent(name))

                if not_a_game.lower() == "yes":
                    logger.info(f"Marking game as not a game: {name}")
                    self.store.add_event(MarkGameAsOtherEvent(name))

                if different_game.lower() != "":
                    logger.info(
                        f"Marking game as different game: {name} -> {different_game}"
                    )
                    self.store.add_event(RenameGameEvent(name, different_game))

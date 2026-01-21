import csv
import logging
from pathlib import Path
from typing import Generator
from models.event import MarkGameCompleteEvent, MarkGameAsOtherEvent, RenameGameEvent
from models.event import Event
from services.store import Store


logger = logging.getLogger(__name__)


class ReadGameStateFormCommand:
    def __init__(self):
        pass

    def execute(self, csv_file_path: Path) -> Generator[Event, None, None]:
        with open(csv_file_path) as csv_file:
            for name, _, complete, not_a_game, different_game in csv.reader(csv_file):
                if complete.lower() == "yes":
                    logger.info(f"Marking game complete: {name}")
                    yield MarkGameCompleteEvent(name)

                if not_a_game.lower() == "yes":
                    logger.info(f"Marking game as not a game: {name}")
                    yield MarkGameAsOtherEvent(name)

                if different_game.lower() != "":
                    logger.info(
                        f"Marking game as different game: {name} -> {different_game}"
                    )
                    yield RenameGameEvent(name, different_game)

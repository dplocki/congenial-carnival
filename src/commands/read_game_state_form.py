import csv
from datetime import datetime
import logging
from typing import Generator
from models.event import MarkGameCompleteEvent, MarkGameAsOtherEvent, RenameGameEvent
from models.event import Event


logger = logging.getLogger(__name__)


class ReadGameStateFormCommand:
    def __init__(self):
        pass

    def execute(
        self, csv_content: str, file_time: datetime = None
    ) -> Generator[Event, None, None]:
        source = iter(csv.reader(csv_content.splitlines()))
        next(iter(source))  # Skip header

        for name, _, complete, not_a_game, different_game in source:
            if complete.lower() == "true":
                logger.info(f"Marking game complete: {name}")
                yield MarkGameCompleteEvent(name, timestamp=file_time)

            if not_a_game.lower() == "true":
                logger.info(f"Marking game as not a game: {name}")
                yield MarkGameAsOtherEvent(name, timestamp=file_time)

            if different_game.lower() != "":
                logger.info(
                    f"Marking game as different game: {name} -> {different_game}"
                )
                yield RenameGameEvent(name, different_game, timestamp=file_time)

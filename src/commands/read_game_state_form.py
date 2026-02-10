import csv
import logging
from typing import Generator
from models.event import MarkGameCompleteEvent, MarkGameAsOtherEvent, RenameGameEvent
from models.event import Event


logger = logging.getLogger(__name__)


class ReadGameStateFormCommand:
    def __init__(self):
        pass

    def execute(self, csv_content) -> Generator[Event, None, None]:
        source = iter(csv.reader(csv_content))
        next(iter(source))  # Skip header

        for name, _, complete, not_a_game, different_game in source:
            if complete.lower() == "True":
                logger.info(f"Marking game complete: {name}")
                yield MarkGameCompleteEvent(name)

            if not_a_game.lower() == "True":
                logger.info(f"Marking game as not a game: {name}")
                yield MarkGameAsOtherEvent(name)

            if different_game.lower() != "":
                logger.info(
                    f"Marking game as different game: {name} -> {different_game}"
                )
                yield RenameGameEvent(name, different_game)

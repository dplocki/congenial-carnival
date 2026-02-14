import logging
from typing import Generator
from services.entries_reducer import EntriesReducer
from services.how_long_to_beat import HowLongToBeat
from models.event import Event, AddGameCompletionTimeEvent


logger = logging.getLogger(__name__)


class AddGameFinishTimeCommand:
    def __init__(
        self, entries_reducer: EntriesReducer, how_long_to_beat: HowLongToBeat
    ):
        self.entries_reducer = entries_reducer
        self.how_long_to_beat = how_long_to_beat

    def execute(self) -> Generator[Event, None, None]:
        for entry in self.entries_reducer.get_all_entries():
            if not entry.is_game or not entry.is_complete:
                continue

            if entry.time_to_complete is not None:
                continue

            logger.info(f"Processing game: {entry.name}")
            result_time = self.how_long_to_beat.fetch_hltb_time(entry.name)
            if result_time is None:
                logger.info(
                    f"Found completion time for {entry.name} has not been found"
                )
                continue

            yield AddGameCompletionTimeEvent(entry.name, result_time)

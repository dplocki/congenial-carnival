import json
import logging
from pathlib import Path
from datetime import datetime

from commands.refresh_epic_games import RefreshEpicGamesCommand
from commands.refresh_gog_games import RefreshGogGamesCommand
from services.command_bus import CommandBus


logger = logging.getLogger(__name__)


class InputDataLoader:
    def __init__(self, command_bus: CommandBus):
        self.command_bus = command_bus

    def load(self):
        json_input_files = sorted(Path("input_data").glob("*.json"))

        for file_path in json_input_files:
            with open(file_path, "r") as file:
                command_handler = None
                if file_path.name.endswith("epic_games.json"):
                    command_handler = RefreshEpicGamesCommand
                elif file_path.name.endswith("gog_games.json"):
                    command_handler = RefreshGogGamesCommand
                else:
                    logger.warning(f"Unknown input file: {file_path.name}")
                    continue

                date_string = file_path.name.split("_")[0]
                data_time_value = datetime.strptime(date_string, "%Y%m%d")

                self.command_bus.handle(
                    command_handler, json.loads(file.read()), data_time_value
                )

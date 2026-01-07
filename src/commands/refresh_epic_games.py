import logging
from typing import Iterable
from models.event import AddEpicGameEvent, DeleteGameEvent
from models.game_location import GameLocation
from services.games import Games


logger = logging.getLogger(__name__)


class RefreshEpicGamesCommand:
    def __init__(self, games: Games):
        self.games = games

    def execute(self, games_titles: Iterable[str]) -> None:
        existing_titles = set(
            game.name
            for game in self.games.get_all_games()
            if GameLocation.EPIC in game.available
        )

        for title in set(games_titles) ^ existing_titles:
            if title in existing_titles:
                logger.info(f"Removing game from Epic: {title}")
                self.games.remove_game(DeleteGameEvent(title, GameLocation.EPIC))
            else:
                logger.info(f"Adding new game on Epic: {title}")
                self.games.add_game(AddEpicGameEvent(title))

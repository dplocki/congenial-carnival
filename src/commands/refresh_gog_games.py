import logging
from operator import attrgetter
from typing import Dict, Iterable
from models.event import AddGogGameEvent, DeleteGogGameEvent
from models.game_location import GameLocation
from services.config import Configuration
from services.games import Games


logger = logging.getLogger(__name__)
get_name = attrgetter("name")


class RefreshGogGamesCommand:
    def __init__(self, config: Configuration, games: Games):
        self.config = config
        self.games = games

    def execute(self, games_data: Iterable[Dict]) -> None:
        already_own_games = set(
            map(
                get_name,
                filter(
                    lambda g: GameLocation.GOG in g.available,
                    self.games.get_all_games(),
                ),
            )
        )

        for game_datum in games_data:
            title = game_datum["title"]
            if title in already_own_games:
                already_own_games.remove(title)
                continue

            logger.info(f"Adding new game on Gog: {title}")
            self.games.add_game(AddGogGameEvent(title, game_datum["id"]))

        for game_name in already_own_games:
            logger.info(f"Removing game from Gog: {game_name}")
            self.games.remove_game(DeleteGogGameEvent(game_name))

import logging
from operator import attrgetter
from typing import Dict, Iterable
from models.event import AddGogGameEvent, DeleteGogGameEvent, MarkGameCompleteEvent
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
            if title not in already_own_games:
                logger.info(f"Adding new game on Gog: {title}")
                self.games.add_game(AddGogGameEvent(title, game_datum["id"]))

            game = self.games.get_game(title)
            if not game.id_complete and "COMPLETED" in game_datum["tags"]:
                logger.info(f"Game complete: {title} (Gog)")
                self.games.change_game_state(MarkGameCompleteEvent(title))

                already_own_games.remove(title)
                continue

        for game_name in already_own_games:
            logger.info(f"Removing game from Gog: {game_name}")
            self.games.remove_game(DeleteGogGameEvent(game_name))

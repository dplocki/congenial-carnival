import logging
from operator import attrgetter

from models.event import AddSteamGameEvent, DeleteSteamGameEvent
from models.game_location import GameLocation
from services.games import Games
from services.steam_api import SteamApi


get_name = attrgetter("name")
logger = logging.getLogger(__name__)


class RefreshSteamGamesCommand:

    def __init__(self, games: Games, steam_api: SteamApi):
        self.games = games
        self.steam_api = steam_api

    def execute(self):
        already_own_games = set(
            map(
                get_name,
                filter(
                    lambda g: GameLocation.STEAM in g.available,
                    self.games.get_all_games(),
                ),
            )
        )

        for game in self.steam_api.get_owned_games():
            game_name = game["name"]
            if game_name in already_own_games:
                already_own_games.remove(game_name)
                continue

            logger.info(f"Adding new game on Steam: {game_name}")
            self.games.add_game(
                AddSteamGameEvent(
                    name=game_name,
                    api_id=game["appid"],
                    last_played=game["rtime_last_played"],
                )
            )

        for game_name in already_own_games:
            logger.info(f"The game as not available on Steam anymore: {game_name}")
            self.games.remove_game(DeleteSteamGameEvent(name=game_name))

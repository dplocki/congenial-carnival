import logging
from operator import attrgetter

from models.event import AddSteamGameEvent, DeleteSteamGameEvent, EventType
from models.game_location import GameLocation
from services.steam_api import SteamApi
from services.store import Store


get_name = attrgetter("name")
logger = logging.getLogger(__name__)


class RefreshSteamGamesCommand:

    def __init__(self, store: Store, steam_api: SteamApi):
        self.store = store
        self.steam_api = steam_api

    def execute(self):
        already_own_games = set(
            event.name
            for event in self.store.get_all_events()
            if event.type == EventType.ADD_GAME and event.where_is == GameLocation.STEAM
        )

        for game in self.steam_api.get_owned_games():
            game_name = game["name"]
            if game_name in already_own_games:
                already_own_games.remove(game_name)
                continue

            logger.info(f"Adding new game on Steam: {game_name}")
            yield AddSteamGameEvent(
                name=game_name,
                api_id=game["appid"],
                last_played=game["rtime_last_played"],
            )

        for game_name in already_own_games:
            logger.info(f"The game as not available on Steam anymore: {game_name}")
            yield DeleteSteamGameEvent(game_name)

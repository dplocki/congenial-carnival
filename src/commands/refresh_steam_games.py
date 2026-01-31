import logging
from operator import attrgetter

from models.event import AddSteamGameEvent, DeleteSteamGameEvent, EventType
from models.game_location import GameLocation
from services.entries_reducer import EntriesReducer
from services.steam_api import SteamApi


get_name = attrgetter("name")
logger = logging.getLogger(__name__)


class RefreshSteamGamesCommand:

    def __init__(self, entries_reducer: EntriesReducer, steam_api: SteamApi):
        self.entries_reducer = entries_reducer
        self.steam_api = steam_api

    def execute(self):
        already_own_games = set(
            name
            for entry in self.entries_reducer.get_all_entries()
            for name in entry.all_names
            if GameLocation.STEAM in entry.available and entry.is_game
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

from operator import attrgetter
from typing import Set

from models.event import AddSteamGameEvent
from services.games import Games
from services.steam_api import SteamApi


get_name = attrgetter("name")


class RefreshSteamGamesCommand:

    def __init__(self, games: Games, steam_api: SteamApi):
        self.games = games
        self.steam_api = steam_api

    def execute(self):
        already_own_games: Set[str] = set(map(get_name, self.games.get_all_games()))
        for game in self.steam_api.get_owned_games():
            if game["name"] in already_own_games:
                continue

            self.games.add_game(
                AddSteamGameEvent(
                    name=game["name"],
                    api_id=game["appid"],
                    last_played=game["rtime_last_played"],
                )
            )

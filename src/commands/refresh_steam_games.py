from operator import attrgetter

from models.game import Game
from services.games import Games
from services.steam_store import SteamStore


get_name = attrgetter("name")


class RefreshSteamGamesCommand:
    def __init__(self, games: Games, steam_store: SteamStore):
        self.games = games
        self.steam_store = steam_store

    def execute(self):
        already_own_games = set(map(get_name, self.games.get_all_games()))
        for game in self.steam_store.get_owned_games():
            if get_name(game) in already_own_games:
                continue

            self.games.add_game(Game(name=get_name(game)))

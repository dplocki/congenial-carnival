from operator import attrgetter

from models.game import Game
from services.games import Games
from services.steam_store import SteamStore


class RefreshGamesCommand:
    def __init__(self, games: Games, steam_store: SteamStore):
        self.games = games
        self.steam_store = steam_store

    def execute(self):
        games = set(map(attrgetter("name"), self.games.get_all_games()))
        for game in self.steam_store.get_owned_games():
            if game["name"] in games:
                continue

            self.games.add_game(Game(name=game["name"]))

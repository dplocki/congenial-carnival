from services.games import Games


class OwnedGamesQuery:
    def __init__(self, games: Games):
        self._games = games

    def execute(self):
        games = list(self._games.get_all_games())
        games.sort(key=lambda g: g.name.lower())

        print("Name, Complete, Platforms")
        for game in games:
            print(f'"{game.name}", {game.is_complete}, {' '.join(game.available)}')

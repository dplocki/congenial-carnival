from services.games import Games


class GameStateFormQuery:
    def __init__(self, games: Games):
        self._games = games

    def execute(self):
        games = list(self._games.get_all_games())
        games.sort(key=lambda g: g.name.lower())

        print("Name,Platforms,Complete,Is not a game,Is different game")
        for game in games:
            print(
                f'"{game.name}", {" ".join(game.available)}, {"Yes" if game.is_complete else "No"},No,'
            )

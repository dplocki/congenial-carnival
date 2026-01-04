from services.config import Configuration
from services.games import Games


class RefreshGogGamesCommand:
    def __init__(self, config: Configuration, games: Games):
        self.config = config
        self.games = games

    def execute(self):
        pass

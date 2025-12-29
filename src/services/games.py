from typing import Iterable
from models.event import AddGameEvent
from models.game import Game
from services.store import Store


class Games:

    def __init__(self, store: Store):
        self.store = store
        self.games = None

    def get_all_games(self) -> Iterable[Game]:
        if self.games is None:
            self.games = []

        return self.games

    def add_game(self, event: AddGameEvent) -> None:
        self.store.add_event(event)

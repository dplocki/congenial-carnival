from typing import Iterable
from models.game import Game
from services.store import Store


class Games:

    def __init__(self, store: Store):
        self.store = store

    def get_all_games(self) -> Iterable[Game]:
        return []

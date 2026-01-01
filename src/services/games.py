from typing import Dict, Iterable
from models.event import AddGameEvent, DeleteGameEvent
from models.game import Game
from services.store import Store


class Games:

    def __init__(self, store: Store):
        self.store = store
        self.games: Dict[str, Game] = None

    def get_all_games(self) -> Iterable[Game]:
        if self.games is None:
            self.games = {}

            for event in self.store.get_all_events():
                game_name = event["name"]

                if game_name not in self.games:
                    self.games[game_name] = Game(event["name"])

                self.games[game_name].available.append(event["where_is"])

        return self.games.values()

    def add_game(self, event: AddGameEvent) -> None:
        self.store.add_event(event)
        self.games = None

    def remove_game(self, event: DeleteGameEvent) -> None:
        self.store.add_event(event)
        self.games = None

from typing import Dict, Iterable
from models.event import AddGameEvent, DeleteGameEvent, EventType, MarkGameCompleteEvent
from models.game import Game
from services.store import Store


class Games:

    def __init__(self, store: Store):
        self.store = store
        self.games: Dict[str, Game] = None

    def get_all_games(self) -> Iterable[Game]:
        if self.games is None:
            self.__build_games_directory()

        return self.games.values()

    def get_game(self, title: str) -> Game:
        if self.games is None:
            self.__build_games_directory()

        return self.games.get(title, None)

    def add_game(self, event: AddGameEvent) -> None:
        self.store.add_event(event)
        self.games = None

    def remove_game(self, event: DeleteGameEvent) -> None:
        self.store.add_event(event)
        self.games = None

    def change_game_state(self, event: MarkGameCompleteEvent) -> None:
        self.store.add_event(event)
        self.games = None

    def __build_games_directory(self) -> None:
        self.games = {}

        for event in self.store.get_all_events():
            if event["type"] == EventType.ADD_GAME:
                game_name = event["name"]

                if game_name not in self.games:
                    self.games[game_name] = Game(event["name"])

                self.games[game_name].available.append(event["where_is"])

            elif event["type"] == EventType.DELETE_GAME:
                game_name = event["name"]
                location = event["where_is"]

                if game_name not in self.games:
                    continue

                self.games[game_name].available.remove(location)
                if not self.games[game_name].available:
                    del self.games[game_name]

            elif event["type"] == EventType.COMPLETED_GAME:
                game_name = event["name"]
                game = self.games[game_name]
                self.games[game_name] = Game(
                    game.name, game.available, is_complete=True
                )

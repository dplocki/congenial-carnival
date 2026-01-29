from typing import Dict, Iterable
from models.event import EventType
from models.entry import Entry
from models.event import Event
from services.store import Store


class EntriesReducer:

    def __init__(self, store: Store):
        self.store = store
        self.entries: Dict[str, Entry] = None

    def get_all_entries(self) -> Iterable[Entry]:
        if self.entries is None:
            self.__build_games_directory()

        return self.entries.values()

    def __build_games_directory(self) -> None:
        self.entries = {}

        for event in self.store.get_all_events():
            self.__reduce_event(event)

    def __reduce_event(self, event: Event) -> None:
        if event["type"] == EventType.ADD_GAME:
            game_name = event["name"]

            if game_name not in self.entries:
                self.entries[game_name] = Entry(game_name)
                self.entries[game_name].all_names.add(game_name)

            self.entries[game_name].available.add(event["where_is"])

        elif event["type"] == EventType.DELETE_GAME:
            game_name = event["name"]
            location = event["where_is"]

            if game_name not in self.entries:
                return

            self.entries[game_name].available.remove(location)
            if not self.entries[game_name].available:
                del self.entries[game_name]

        elif event["type"] == EventType.COMPLETED_GAME:
            game_name = event["name"]
            game = self.entries[game_name]
            self.entries[game_name] = Entry(game.name, game.available, is_complete=True)

        elif event["type"] == EventType.RENAME_GAME:
            old_game_name = event["old_name"]
            new_game_name = event["new_name"]

            new_game = self.entries.get(new_game_name, Entry(name=new_game_name))

            old_game = self.entries[old_game_name]
            new_all_names = old_game.all_names | new_game.all_names

            new_available = old_game.available | new_game.available
            new_is_complete = old_game.is_complete or new_game.is_complete
            new_is_game = old_game.is_game or old_game.is_game

            self.entries[new_game_name] = Entry(
                name=new_game_name,
                all_names=new_all_names,
                available=new_available,
                is_complete=new_is_complete,
                is_game=new_is_game,
            )

            del self.entries[old_game_name]

from dataclasses import dataclass, field
from typing import Set
from models.game_location import GameLocation


@dataclass(frozen=True)
class Entry:
    name: str
    available: Set[GameLocation] = field(default_factory=set)
    all_names: Set[str] = field(default_factory=set)
    is_complete: bool = field(default=False)
    is_game: bool = field(default=True)

    def __post_init__(self):
        self.all_names.add(self.name)

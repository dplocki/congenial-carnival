from dataclasses import dataclass, field
from typing import Set
from models.game_location import GameLocation


@dataclass(frozen=True)
class Game:
    name: str
    available: Set[GameLocation] = field(default_factory=set)
    aliases: Set[str] = field(default_factory=set)
    is_complete: bool = False

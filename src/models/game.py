from dataclasses import dataclass, field
from models.game_location import GameLocation


@dataclass(frozen=True)
class Game:
    name: str
    available: list[GameLocation] = field(default_factory=list)
    id_complete: bool = False

from dataclasses import dataclass
from models.note_type import NoteType
from .event import Event
from models.event import EventType


@dataclass(frozen=True, init=False)
class AddNoteToGame(Event):
    game_name: str
    note_type: NoteType

    def __init__(self, game_name: str, note_type: NoteType, timestamp: int = None):
        super().__init__(EventType.ADD_NOTE, timestamp)
        object.__setattr__(self, "game_name", game_name)
        object.__setattr__(self, "note_type", note_type)

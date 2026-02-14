from enum import StrEnum


class EventType(StrEnum):
    ADD_GAME = "add_game"
    ADD_NOTE = "add_note"
    COMPLETED_GAME = "completed_game"
    DELETE_GAME = "delete_game"
    MARK_AS_NOT_GAME = "mark_as_not_game"
    RENAME_GAME = "rename_game"
    ADD_COMPLETION_TIME = "add_completion_time"

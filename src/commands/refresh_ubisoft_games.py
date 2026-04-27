import logging
from commands.refresh_games_by_simple_list import RefreshGamesBySimpleListCommand
from models.game_location import GameLocation
from services.entries_reducer import EntriesReducer

logger = logging.getLogger(__name__)


class RefreshUbisoftGamesCommand(RefreshGamesBySimpleListCommand):

    def __init__(self, entries_reducer: EntriesReducer):
        super().__init__(GameLocation.UBISOFT, entries_reducer)

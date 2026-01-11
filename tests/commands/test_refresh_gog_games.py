from unittest.mock import Mock
from src.commands.refresh_gog_games import RefreshGogGamesCommand
from models.event import AddGogGameEvent, MarkGameCompleteEvent
from models.game_location import GameLocation
from tests.utils.data_providers import generate_game, generate_int, generate_str


def build_add_gog_game_event(title: str, gog_id: int = None) -> dict:
    return AddGogGameEvent(name=title, gog_id=gog_id or generate_int())


def build_mark_game_complete_event(title: str) -> dict:
    return MarkGameCompleteEvent(name=title)


def build_gog_game_entity(
    title: str, gog_id: int = None, is_complete: bool = False
) -> dict:
    return {
        "title": title,
        "id": gog_id or generate_int(),
        "tags": ["COMPLETED"] if is_complete else [],
    }


def test_adds_new_gog_game_when_not_owned():
    new_game_name = generate_str()
    new_game_id = generate_int()

    store = Mock()
    store.get_all_events.return_value = []

    cmd = RefreshGogGamesCommand(store)
    cmd.execute([build_gog_game_entity(new_game_name, new_game_id)])

    store.add_event.assert_called_once()
    event = store.add_event.call_args[0][0]
    assert isinstance(event, AddGogGameEvent)
    assert event.name == new_game_name and event.gog_id == new_game_id


def test_skips_existing_gog_game():
    owned_game_name = generate_str()

    store = Mock()
    store.get_all_events.return_value = [build_add_gog_game_event(owned_game_name)]

    cmd = RefreshGogGamesCommand(store)
    cmd.execute([build_gog_game_entity(owned_game_name, is_complete=True)])

    store.add_event.assert_not_called()


def test_marks_existing_game_complete():
    owned_game_name = generate_str()

    store = Mock()
    store.get_all_events.return_value = [build_add_gog_game_event(owned_game_name)]

    cmd = RefreshGogGamesCommand(store)
    cmd.execute([build_gog_game_entity(owned_game_name, is_complete=True)])

    store.change_game_state.assert_called_once()
    evt = store.change_game_state.call_args[0][0]
    assert isinstance(evt, MarkGameCompleteEvent) and evt.name == owned_game_name


def test_does_not_mark_if_already_complete():
    owned_game_name = generate_str()

    store = Mock()
    store.get_all_events.return_value = [
        build_add_gog_game_event(owned_game_name),
        build_mark_game_complete_event(owned_game_name),
    ]

    cmd = RefreshGogGamesCommand(config=Mock(), games=store)
    cmd.execute([build_gog_game_entity(owned_game_name, is_complete=True)])

    store.add_event.assert_not_called()

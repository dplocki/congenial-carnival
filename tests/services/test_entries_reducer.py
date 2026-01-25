from unittest.mock import Mock

from models.event import EventType
from models.game_location import GameLocation
from services.entries_reducer import EntriesReducer
from tests.utils.asserts import are_collections_equal
from tests.utils.data_providers import generate_enum, generate_str


def test_get_all_entries_empty():
    store = Mock()
    store.get_all_events.return_value = []

    entries_reducer = EntriesReducer(store)

    first_time_all_entries = list(entries_reducer.get_all_entries())
    second_time_all_entries = list(entries_reducer.get_all_entries())

    assert first_time_all_entries == []
    assert store.get_all_events.call_count == 1
    assert are_collections_equal(first_time_all_entries, second_time_all_entries)


def test_get_all_entries_aggregates_events():
    single_game_title = generate_str()
    repeating_game_title = generate_str()

    store = Mock()
    store.get_all_events.return_value = [
        {
            "type": EventType.ADD_GAME,
            "name": repeating_game_title,
            "where_is": GameLocation.STEAM,
        },
        {
            "type": EventType.ADD_GAME,
            "name": single_game_title,
            "where_is": GameLocation.OTHER,
        },
        {
            "type": EventType.ADD_GAME,
            "name": repeating_game_title,
            "where_is": GameLocation.GOG,
        },
    ]

    entries_reducer = EntriesReducer(store)
    all_entries = list(entries_reducer.get_all_entries())

    assert len(all_entries) == 2

    game_from_two_sources = next(g for g in all_entries if g.name == repeating_game_title)
    assert GameLocation.STEAM in game_from_two_sources.available
    assert GameLocation.GOG in game_from_two_sources.available

    game_from_single_sources = next(g for g in all_entries if g.name == single_game_title)
    assert game_from_single_sources.available == {GameLocation.OTHER}


def test_deleted_games_should_not_appear():
    removed_game_title = generate_str()
    removed_game_location = generate_enum(GameLocation)
    store = Mock()
    store.get_all_events.return_value = [
        {
            "type": EventType.ADD_GAME,
            "name": removed_game_title,
            "where_is": removed_game_location,
        },
        {
            "type": EventType.DELETE_GAME,
            "name": removed_game_title,
            "where_is": removed_game_location,
        },
    ]

    entries_reducer = EntriesReducer(store)

    get_all_entries = list(entries_reducer.get_all_entries())

    assert len(get_all_entries) == 0


def test_deleted_games_should_affect_only_game_location():
    removed_game_title = generate_str()
    store = Mock()
    store.get_all_events.return_value = [
        {
            "type": EventType.ADD_GAME,
            "name": removed_game_title,
            "where_is": GameLocation.GOG,
        },
        {
            "type": EventType.ADD_GAME,
            "name": removed_game_title,
            "where_is": GameLocation.STEAM,
        },
        {
            "type": EventType.DELETE_GAME,
            "name": removed_game_title,
            "where_is": GameLocation.STEAM,
        },
    ]

    entries_reducer = EntriesReducer(store)
    all_entries = list(entries_reducer.get_all_entries())

    assert len(all_entries) == 1
    assert all_entries[0].available == {GameLocation.GOG}


def test_game_marks_game_as_complete():
    completed_game_title = generate_str()
    store = Mock()
    store.get_all_events.return_value = [
        {
            "type": EventType.ADD_GAME,
            "name": completed_game_title,
            "where_is": generate_enum(GameLocation),
        },
        {
            "type": EventType.COMPLETED_GAME,
            "name": completed_game_title,
        },
    ]

    entries_reducer = EntriesReducer(store)
    all_entries = list(entries_reducer.get_all_entries())

    game = all_entries[0]

    assert game is not None
    assert game.is_complete


def test_rename_should_reduce_game_set():
    old_name = generate_str()
    new_name = generate_str()
    game_location = generate_enum(GameLocation)
    store = Mock()
    store.get_all_events.return_value = [
        {
            "type": EventType.ADD_GAME,
            "name": old_name,
            "where_is": game_location,
        },
        {
            "type": EventType.RENAME_GAME,
            "old_name": old_name,
            "new_name": new_name,
        },
    ]

    entries_reducer = EntriesReducer(store)
    all_entries = list(entries_reducer.get_all_entries())

    assert len(all_entries) == 1
    game = all_entries[0]
    assert game.name == new_name
    assert len(game.aliases) == 1
    assert old_name in game.aliases
    assert len(game.available) == 1
    assert game.available == {game_location}


def test_rename_should_reduce_games_set():
    gog_name = generate_str()
    steam_name = generate_str()
    store = Mock()
    store.get_all_events.return_value = [
        {
            "type": EventType.ADD_GAME,
            "name": gog_name,
            "where_is": GameLocation.GOG,
        },
        {
            "type": EventType.ADD_GAME,
            "name": steam_name,
            "where_is": GameLocation.STEAM,
        },
        {
            "type": EventType.RENAME_GAME,
            "old_name": steam_name,
            "new_name": gog_name,
        },
    ]

    entries_reducer = EntriesReducer(store)
    all_entries = list(entries_reducer.get_all_entries())

    assert len(all_entries) == 1
    game = all_entries[0]
    assert game.name == gog_name
    assert len(game.available) == 2
    assert GameLocation.GOG in game.available
    assert GameLocation.STEAM in game.available
    assert len(game.aliases) == 1
    assert steam_name in game.aliases

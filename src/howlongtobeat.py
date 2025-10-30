from howlongtobeatpy import HowLongToBeat


def fetch_hltb_time(game_name: str) -> int | None:
    """
    Given a game name, return the main story completion time in hours from HowLongToBeat.
    Returns None if not found.
    """
    results = HowLongToBeat().search(game_name)
    if not results:
        return None

    best = max(results, key=lambda x: x.similarity)
    return best.main_story if best.main_story else None

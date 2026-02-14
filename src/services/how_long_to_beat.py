from howlongtobeatpy import SearchModifiers, HowLongToBeat as HLTB


class HowLongToBeat:
    def __init__(self):
        self.hltb = HLTB()

    def fetch_hltb_time(self, game_name: str) -> int | None:
        results = self.hltb.search(
            game_name=game_name,
            similarity_case_sensitive=False,
            search_modifiers=SearchModifiers.HIDE_DLC,
        )
        if not results:
            return None

        best = max(results, key=lambda r: r.similarity)
        return best.completionist if best.completionist else None

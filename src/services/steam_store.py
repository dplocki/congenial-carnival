import requests


class SteamStore:
    STEAM_BASE_URL = "http://api.steampowered.com"

    def __init__(self, api_key: str, steam_id: str):
        self.api_key = api_key
        self.steam_id = steam_id
        self.base_url = "http://api.steampowered.com"

    def get_game_details(self, app_id: str):
        url = f"https://store.steampowered.com/api/appdetails"
        params = {"appids": app_id}

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if str(app_id) in data and data[str(app_id)]["success"]:
            return data[str(app_id)]["data"]

        return {}

    def get_owned_games(self):
        url = f"{SteamStore.STEAM_BASE_URL}/IPlayerService/GetOwnedGames/v0001/"
        params = {
            "key": self.api_key,
            "steamid": self.steam_id,
            "format": "json",
            "include_appinfo": 1,
            "include_played_free_games": 1,
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if "response" in data and "games" in data["response"]:
            return data["response"]["games"]

        return []

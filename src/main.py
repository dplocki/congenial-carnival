import requests


STEAM_BASE_URL = "http://api.steampowered.com"
API_KEY = "YOUR_STEAM_API_KEY"
STEAM_ID = "YOUR_STEAM_ID"


def get_owned_games(self):
    url = f"{STEAM_BASE_URL}/IPlayerService/GetOwnedGames/v0001/"
    params = {
        "key": self.api_key,
        "steamid": self.steam_id,
        "format": "json",
        "include_appinfo": 1,
        "include_played_free_games": 1,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if "response" in data and "games" in data["response"]:
            return data["response"]["games"]
        else:
            return []

    except requests.exceptions.RequestException as e:
        print(f"Error fetching games: {e}")


def main():
    print("Helo World!")


if __name__ == "__main__":
    main()

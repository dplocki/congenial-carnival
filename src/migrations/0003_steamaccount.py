from yoyo import step

__depends__ = {"0002_howlongtobeat"}

steps = [
    step(
        """
        CREATE TABLE steam (
            game_id INTEGER PRIMARY KEY,
            steam_appid INTEGER,
            steam_data TEXT,
            FOREIGN KEY (game_id) REFERENCES games(id) ON DELETE CASCADE
        )
        """,
        "DROP TABLE steam",
    ),
]

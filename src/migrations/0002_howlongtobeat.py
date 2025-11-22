from yoyo import step

__depends__ = {"0001_initial"}

steps = [
    step(
        """
        CREATE TABLE howlongtobeat (
            id INTEGER PRIMARY KEY,
            main_story INTEGER,
            main_plus_extras INTEGER,
            completionist INTEGER,
            FOREIGN KEY (id) REFERENCES games(id) ON DELETE CASCADE
        )
        """,
        "DROP TABLE howlongtobeat",
    ),
    step(
        """
        CREATE TABLE games_new (
            id INTEGER PRIMARY KEY,
            name TEXT
        )
        """,
        "DROP TABLE games_new",
    ),
    step(
        """
        INSERT INTO games_new (id, name)
        SELECT id, name FROM games
        """,
        "DELETE FROM games_new",
    ),
    step(
        "DROP TABLE games",
        "CREATE TABLE games (id INTEGER PRIMARY KEY, name TEXT, howlongtobeat INTEGER)",
    ),
    step(
        "ALTER TABLE games_new RENAME TO games", "ALTER TABLE games RENAME TO games_new"
    ),
]

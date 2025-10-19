from yoyo import step

step(
    """
CREATE TABLE games (
    id INTEGER PRIMARY KEY,
    name TEXT,
    howlongtobeat INTEGER
)
""",
    "DROP TABLE games",
)

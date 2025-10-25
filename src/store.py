import sqlite3
from yoyo import get_backend, read_migrations


class Store:
    def __init__(self, db_file_path: str):
        self.db_file_path = db_file_path

    def migrate_database(self):
        backend = get_backend(f"sqlite:///{self.db_file_path}")
        migrations = read_migrations("./src/migrations")

        with backend.lock():
            backend.apply_migrations(backend.to_apply(migrations))

    def get_stored_games(self):
        with sqlite3.connect(self.db_file_path) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id, name, howlongtobeat FROM games")
            return cursor.fetchall()

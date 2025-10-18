from yoyo import get_backend, read_migrations
from config import load_config
from steam import SteamGamesApi


def migrate_database(db_file_path: str):
    backend = get_backend(f"sqlite:///{db_file_path}")
    migrations = read_migrations("./src/migrations")

    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))


if __name__ == "__main__":
    migrate_database("database.db")

    config = load_config().config
    result = SteamGamesApi(config["steam_api_key"], config["steam_id"])
    print(config, result.get_owned_games())

from config import load_config
from store import migrate_database


if __name__ == "__main__":
    config = load_config()
    migrate_database(config.get_database_path())

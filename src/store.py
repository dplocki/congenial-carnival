from yoyo import get_backend, read_migrations


def migrate_database(db_file_path: str):
    backend = get_backend(f"sqlite:///{db_file_path}")
    migrations = read_migrations("./src/migrations")

    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))

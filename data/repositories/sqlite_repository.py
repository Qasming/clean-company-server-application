from infrastructure.sqlite_connection import SqliteConnection


class SqliteRepository:
    def __init__(self, db_connection: SqliteConnection):
        self._db = db_connection

    @property
    def db(self) -> SqliteConnection:
        return self._db

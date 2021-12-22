from abc import abstractmethod
from infrastructure.sqlite_connection import SqliteConnection


class Seeder:
    def __init__(self, connection: SqliteConnection):
        self._db = connection

    @abstractmethod
    def seed(self):
        pass

    @property
    def db(self) -> SqliteConnection:
        return self._db

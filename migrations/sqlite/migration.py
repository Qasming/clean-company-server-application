from abc import abstractmethod, ABC
from sqlite3 import Connection


class Migration(ABC):
    def __init__(self, db: Connection):
        self._db = db

    @abstractmethod
    def migrate(self):
        pass

    @abstractmethod
    def rollback(self):
        pass

    @property
    def db(self) -> Connection:
        return self._db

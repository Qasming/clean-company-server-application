from sqlite3 import Connection, Cursor
import sqlite3
from typing import List


class SqliteCursor:
    _cursor: Cursor = None

    def __init__(self, cursor: Cursor):
        self._cursor = cursor

    def fetchone(self) -> dict:
        return self._cursor.fetchone()

    def fetchall(self) -> List[dict]:
        return self._cursor.fetchall()

    def execute(self, query: str, params: dict = {}):
        self._cursor.execute(query, params)

    def close(self):
        self._cursor.close()


class SqliteConnection:
    _connection: Connection

    def __init__(self):
        self._connection = None

    def __del__(self):
        if self._connection is not None:
            self._connection.close()

    def connect(self, filename: str):
        self._connection = sqlite3.connect(filename, check_same_thread=False)
        self._connection.row_factory = sqlite3.Row

    def commit(self) -> None:
        self._connection.commit()

    def cursor(self) -> SqliteCursor:
        return SqliteCursor(self._connection.cursor())

    def close(self) -> None:
        self._connection.close()

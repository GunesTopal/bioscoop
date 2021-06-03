import sqlite3
from sqlite3 import Error
from sqlite3.dbapi2 import Cursor


class dbconn():
    DB_PATH = "data/Databank.db"

    def __init__(self) -> None:
        self.create_connection()

    def __enter__(self) -> Cursor:
        self.create_connection()
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.conn.commit()
        self.conn.close()

    def create_connection(self) -> None:
        try:
            self.conn = sqlite3.connect(self.DB_PATH)
            self.conn.execute("PRAGMA foreign_keys = 1")
            self.conn.row_factory = sqlite3.Row
        except Error as e:
            print("Fout bij connectie met databank: ", e)

    def close_connection(self) -> None:
        self.conn.close()

    def execute_script(self, script: str) -> None:
        with open(script) as sql_file:
            query = sql_file.read()
            self.conn.executescript(query)
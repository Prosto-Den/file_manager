import sqlite3 as sql
from framework.singleton.singleton import Singleton


class Database(metaclass=Singleton):
    __connection: sql.Connection = None

    @classmethod
    def connection(cls) -> sql.Connection:
        return cls.__connection

    @classmethod
    def establish_connection(cls, file_path: str) -> None:
        if cls.__connection is None:
            cls.__connection = sql.connect(file_path, check_same_thread=False)

    @classmethod
    def disconnect(cls) -> None:
        cls.__connection.close()

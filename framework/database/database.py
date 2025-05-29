import sqlite3 as sql
from framework.singleton.singleton import Singleton


class Database(metaclass=Singleton):
    """
    Класс для подключения к БД SQLite
    """
    __connection: sql.Connection = None

    @classmethod
    def connection(cls) -> sql.Connection:
        """
        Объект соединения к БД
        """
        return cls.__connection

    @classmethod
    def establish_connection(cls, file_path: str) -> None:
        """
        Инициирует подключение к БД
        :param file_path: Путь к файлу .db
        """
        if cls.__connection is None:
            cls.__connection = sql.connect(file_path, check_same_thread=False)

    @classmethod
    def disconnect(cls) -> None:
        """
        Отключаемся от БД
        """
        cls.__connection.close()

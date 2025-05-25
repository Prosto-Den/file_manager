import sqlite3 as sql
from dataclasses import dataclass
from typing import Literal


#TODO если будет не лень, вынесу в отдельные SQL-файлы
@dataclass
class HashQueries:
    create_hash_table: str = """create table if not exists Hash(
                                hash TEXT,
                                filepath TEXT,
                                modification_date INTEGER);"""
    select_all: str = "select * from Hash;"
    select_where: str = "select {} from Hash where {};"
    select_all_duplicates: str = """select t.*, dup.filepath as dup_filepath, 
    dup.modification_date as dup_modification_date from Hash t 
    join (select * from Hash group by hash having count(*) > 1) dup 
    on t.hash = dup.hash and t.filepath != dup.filepath;"""
    insert: str = "insert into Hash values(?, ?, ?);"
    delete: str = "delete from Hash where {} = ?;"


class HashModel:
    __conn: sql.Connection = None

    @dataclass
    class Fields:
        hash: str
        file_path: str
        modification_date: int

    @dataclass
    class DuplicateFields:
        hash: str
        file_path: str
        modification_date: int
        duplicate_filepath: str
        duplicate_modification_date: int

    @classmethod
    def __prepare_keys_for_select(cls, keys: list) -> str:
        result = ''
        for i in range((length := len(keys))):
            if i == length - 1:
                result = ''.join([result, f'{keys[i]} = ?;'])
            else:
                result = ''.join([result, f'{keys[i]} = ?,'])
        return result

    @classmethod
    def connect(cls, connection: sql.Connection) -> None:
        cls.__conn = connection

    @classmethod
    def create(cls):
        cursor = cls.__conn.cursor()
        cursor.execute(HashQueries.create_hash_table)
        cls.__conn.commit()

    @classmethod
    def select_all(cls) -> list[Fields]:
        cursor = cls.__conn.cursor()
        cursor.execute(HashQueries.select_all)
        data = cursor.fetchall()
        return [cls.Fields(*item) for item in data]

    @classmethod
    def select_by_filepath(cls, path: str) -> Fields | None:
        cursor = cls.__conn.cursor()
        select_where = HashQueries.select_where.format('*', 'filepath=?')
        cursor.execute(select_where, (path, ))
        data = cursor.fetchone()
        if data is None:
            return None
        return cls.Fields(*data)

    @classmethod
    def select_where(cls, what: Literal['*', 'hash', 'filepath', 'modification_date'],
                     **kwargs) -> Fields | list[Fields]:
        cursor = cls.__conn.cursor()
        select_where = HashQueries.select_where.format(what, cls.__prepare_keys_for_select(list(kwargs.keys())))
        cursor.execute(select_where, tuple(kwargs.values()))
        data = cursor.fetchall()

        return [cls.Fields(*item) for item in data] if len(data) > 1 else cls.Fields(*data[0])

    @classmethod
    def insert(cls, hash_: str, filepath: str, modification_date: str) -> None:
        cursor = cls.__conn.cursor()
        cursor.execute(HashQueries.insert, (hash_, filepath, modification_date))
        cls.__conn.commit()

    @classmethod
    def select_all_duplicates(cls) -> list[DuplicateFields] | None:
        cursor = cls.__conn.cursor()
        cursor.execute(HashQueries.select_all_duplicates)
        data = cursor.fetchall()
        if data is None:
            return None
        return [cls.DuplicateFields(*item) for item in data]

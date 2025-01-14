from typing import Any


class InitException(Exception):
    def __init__(self, value: Any) -> None:
        self.__value = value

    def __str__(self):
        return f'Значение {self.__value.__name__} не инициализировано!'
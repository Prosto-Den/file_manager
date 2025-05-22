from pydantic import BaseModel
from typing import TypeVar, Type
import json


T = TypeVar('T', bound=BaseModel)


class JsonReader:
    @staticmethod
    def read_file_as_model(path_to_file: str, model: Type[T]) -> T:
        with open(path_to_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return model(**data)

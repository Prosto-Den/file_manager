from pydantic import BaseModel
from typing import TypeVar, Type
import json


T = TypeVar('T', bound=BaseModel)


class JsonManip:
    @staticmethod
    def read_file_as_model(path_to_file: str, model: Type[T]) -> T:
        with open(path_to_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return model(**data)

    @staticmethod
    def write_file_from_model(path_to_file: str, model: T) -> None:
        with open(path_to_file, 'w', encoding='utf-8') as file:
            json.dump(model.model_dump(by_alias=True), file, indent=4, ensure_ascii=False)

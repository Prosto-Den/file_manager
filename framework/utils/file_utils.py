from typing import LiteralString, Literal
from framework.utils.time_utils import TimeUtils
from framework.utils.hash_calculator import HashCalculator
import shutil
import os


class FileUtils:
    # TODO при большом количестве файлов удаление происходит медленно, нужно продумать индикацию
    @classmethod
    def delete_file(cls, filepath: str) -> None:
        """
        Удаляет файл/директорию по указанному пути
        :param filepath: Путь к файлу/директории
        :return: None
        """
        if cls.is_dir(filepath):
            #TODO стоит ли добавить предупреждение о непустой папке?
            shutil.rmtree(filepath, ignore_errors=True)
        else:
            os.remove(filepath)

    #TODO сделать через move?
    @staticmethod
    def rename_file(old_filepath: str | bytes | LiteralString, new_filepath: str | bytes | LiteralString) -> None:
        os.rename(old_filepath, new_filepath)

    @staticmethod
    def move_file(old_filepath: str, new_filepath: str) -> None:
        shutil.move(old_filepath, new_filepath)

    @staticmethod
    def copy_file(old_filepath: str, new_filepath: str) -> None:
        shutil.copy2(old_filepath, new_filepath)

    @staticmethod
    def open_file(filepath: str) -> None:
        os.startfile(filepath)

    @staticmethod
    def is_dir(filepath: str) -> bool:
        return os.path.isdir(filepath)

    @staticmethod
    def is_file(filepath: str | bytes | LiteralString) -> bool:
        return os.path.isfile(filepath)

    @staticmethod
    def get_file_info(filepath: str) -> os.stat_result:
        return os.stat(filepath)

    @staticmethod
    def get_modification_date(filepath: str) -> int:
        return os.stat(filepath).st_ctime_ns

    @classmethod
    def calc_hash(cls, filepath: str, buffer_size: int) -> tuple[str, str, int]:
        return HashCalculator.mapped_reader(filepath, buffer_size), filepath, cls.get_modification_date(filepath)

    @staticmethod
    def convert_bytes(size: float) -> str:
        counter = 0
        INFO_SIZES = ('B', 'KB', 'MB', 'GB', 'TB', 'PB')

        while size >= 1024 and counter < len(INFO_SIZES) - 1:
            size /= 1024
            counter += 1

        return f"{size:.2f} {INFO_SIZES[counter]}"

    @classmethod
    def is_empty_dir(cls, path: str) -> bool:
        return len(os.listdir(path)) == 0

    @classmethod
    def read_file(cls, filepath: str, mode: Literal['r', 'rb'] = 'r') -> str | bytes:
        """
        Метод для чтения содержимого файла. Метод загружает все данные из файла в память,
        НЕ ИСПОЛЬЗОВАТЬ ДЛЯ БОЛЬШИХ ФАЙЛОВ!!!
        :param filepath: Путь к файлу
        :param mode: Режим чтения. 'r' - читать как есть, 'rb' - читать, как поток байтов
        :return: Содержимое файла (строка или байты)
        """
        with open(filepath, mode) as file:
            return file.read()

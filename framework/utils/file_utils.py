import hashlib as hl
import shutil
import os
import wx



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
    def rename_file(old_filepath: str, new_filepath: str) -> None:
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
    def is_file(filepath: str) -> bool:
        return os.path.isfile(filepath)

    @staticmethod
    def get_file_info(filepath: str) -> os.stat_result:
        return os.stat(filepath)

    @staticmethod
    def convert_bytes(size: float) -> str:
        counter = 0
        INFO_SIZES = ('B', 'KB', 'MB', 'GB', 'TB', 'PB')

        while size >= 1024 and counter < len(INFO_SIZES) - 1:
            size /= 1024
            counter += 1

        return f"{size:.2f} {INFO_SIZES[counter]}"

    @staticmethod
    def calc_checksum(file_path: str) -> str:
        algorithm = hl.sha1(usedforsecurity=False)

        with open(file_path, 'rb') as file:
            algorithm.update(file.read())

        return algorithm.hexdigest()

    @classmethod
    def is_empty(cls, filepath: str) -> bool:
        return len(os.listdir(filepath)) == 0

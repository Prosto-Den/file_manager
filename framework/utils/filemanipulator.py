import os
import pathlib as pl
import re
import wx
import shutil
import string
from framework.events import PathChangedEvent
from .fileSize import FileSize
from .timeFunc import ns_to_datetime
import datetime as dt


class FileManipulator(wx.FileSystem):
    def __init__(self, filepath: str, event_handler: wx.EvtHandler):
        super().__init__()
        if filepath is None:
            filepath = os.path.dirname(__file__)
        self.ChangePathTo(filepath, True)

        self.__event_handler: wx.EvtHandler = event_handler

        # наблюдатель нужен для отслеживания изменений в файловой системе (удаление/переименование файлов и т.п.)
        # на изменение директории не реагирует
        self.__watcher = wx.FileSystemWatcher()
        self.__watcher.Add(filepath)

    @property
    def watcher(self) -> wx.FileSystemWatcher:
        return self.__watcher

    def change_path_to(self, location: str, is_dir: bool) -> None:
        self.__watcher.RemoveAll()
        self.ChangePathTo(location, True)
        self.__watcher.Add(location)
        wx.PostEvent(self.__event_handler, PathChangedEvent())

    def listdir(self, is_absolute: bool = False) -> list[str]:
        """
        Возвращает список с названиями файлов, которые расположены в директории, куда указывает file manipulator в данный
        момент.
        :param is_absolute: Если True - возвращает список с абсолютными путями к файлам. По умолчанию False.
        :return: Список с названиями файлов
        """
        files = os.listdir(self.GetPath())
        return files if not is_absolute else [self.GetPath() + file for file in files]

    def listdir_with_info(self, is_absolute: bool = False) -> list[tuple[str, int, dt.datetime]]:
        """
        Возвращает список с названиями файлов вместе с дополнительной информацией о них (размер файла + дата последнего
        изменения). Для папок размер всегда 0.
        :param is_absolute: Если True - возвращает список с абсолютными путями к файлам. По умолчанию False.
        :return: Список с названиями файлов вместе с их размерами и датами последнего изменения
        """
        files = self.listdir(is_absolute)
        absolute_file_path = self.listdir(True)
        file_info = [self.get_file_info(file) for file in absolute_file_path]
        sizes = [info.st_size if self.is_file(file) else 0 for file, info in zip(absolute_file_path, file_info)]
        dates = [ns_to_datetime(info.st_ctime_ns) for info in file_info]

        return list(zip(files, sizes, dates))


    def get_absolute_path(self, file: str) -> str:
        """Вернёт абсолютный путь к файлу, если он есть в директории, куда указывает file manipulator,
        иначе вернёт пустую строку.
        :param file: Название файла
        :return: абсолютный путь к файлу или пустая строка"""
        return self.GetPath() + file if file in self.listdir() else ''

    #TODO при большом количестве файлов удаление происходит медленно, нужно продумать индикацию
    @classmethod
    def delete_file(cls, filepath: str) -> None:
        if cls.is_dir(filepath):
            #TODO стоит ли добавить предупреждение о непустой папке?
            shutil.rmtree(filepath, ignore_errors=True)
        else:
            os.remove(filepath)

    def create_folder(self, filepath: str) -> None:
        files = [file for file in self.listdir() if re.match(r'Новая\sпапка\s?\d?', file)]
        if (length := len(files)) == 0:
            filepath = filepath + 'Новая папка'
        else:
            filepath = filepath + f'Новая папка {length}'
        os.mkdir(filepath)

    @staticmethod
    def rename_file(old_filepath: str, new_filepath: str) -> None:
        os.rename(old_filepath, new_filepath)

    @staticmethod
    def move_file(old_filepath: str, new_filepath: str) -> None:
        #TODO проверить
        #Такая же логика работы у метода rename_file. Может быть, нет смысла в отдельной функции
        shutil.move(old_filepath, new_filepath)

    @staticmethod
    def open_file(filepath: str) -> None:
        os.startfile(filepath)

    @staticmethod
    def is_dir(filepath: str) -> bool:
        return pl.Path(filepath).is_dir()

    @staticmethod
    def is_file(filepath: str) -> bool:
        return pl.Path(filepath).is_file()

    @staticmethod
    def get_suffix(filepath: str) -> str:
        return pl.Path(filepath).suffix

    @staticmethod
    def get_logical_drives():
        return ['{}:/'.format(d) for d in string.ascii_uppercase if os.path.exists('{}:'.format(d))]

    @staticmethod
    def get_file_info(filepath: str) -> os.stat_result:
        return pl.Path(filepath).stat()

    @staticmethod
    def convert_bytes(size: float) -> str:
        counter = 0
        INFO_SIZES = ('B', 'KB', 'MB', 'GB', 'TB', 'PB')

        while size >= 1024:
            size /= 1024
            counter += 1

        if counter > len(INFO_SIZES):
            counter = len(INFO_SIZES) - 1

        return f"{size:.2f} {INFO_SIZES[counter]}"
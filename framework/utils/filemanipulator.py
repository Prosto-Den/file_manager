import os
import pathlib as pl
import wx
import shutil
import string
from framework.events import PathChangedEvent


class FileManipulator(wx.FileSystem):
    def __init__(self,  filepath: str, event_handler: wx.EvtHandler):
        super().__init__()
        if filepath is None:
            filepath = os.path.dirname(__file__)
        self.ChangePathTo(filepath, True)

        self.__event_handler = event_handler

        # наблюдатель нужен для отслеживания изменений в файловой системе (удаление/переименование файлов и т.п.)
        # на изменение директории не реагирует
        self.__watcher = wx.FileSystemWatcher()
        self.__watcher.Add(filepath)

    @property
    def watcher(self) -> wx.FileSystemWatcher:
        return self.__watcher

    def change_path_to(self, location: str, is_dir: bool) -> None:
        self.__watcher.RemoveAll()
        self.ChangePathTo(location, is_dir)
        self.__watcher.Add(location)
        wx.PostEvent(self.__event_handler, PathChangedEvent())

    def listdir(self, is_absolute: bool = False) -> list:
        files = os.listdir(self.GetPath())
        return files if not is_absolute else [self.GetPath() + file for file in files]

    def get_absolute_path(self, file: str) -> str:
        return self.GetPath() + file if file in self.listdir() else ''

    #TODO при большом количестве файлов удаление происходит медленно, нужно продумать индикацию
    @classmethod
    def delete_file(cls, filepath: str) -> None:
        if cls.is_dir(filepath):
            #TODO стоит ли добавить предупреждение о непустой папке?
            shutil.rmtree(filepath, ignore_errors=True)
        else:
            os.remove(filepath)

    @staticmethod
    def create_folder(filepath: str) -> None:
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
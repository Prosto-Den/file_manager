import os
import pathlib as pl
import wx
import shutil


class FileManipulator(wx.FileSystem):
    def __init__(self,  filepath: str):
        super().__init__()
        if filepath is None:
            filepath = os.path.dirname(__file__)
        self.ChangePathTo(filepath, True)
        self.__watcher = wx.FileSystemWatcher()
        self.__watcher.Add(filepath)

    @property
    def watcher(self) -> wx.FileSystemWatcher:
        return self.__watcher

    def change_path_to(self, location: str, is_dir: bool) -> None:
        self.__watcher.RemoveAll()
        self.ChangePathTo(location, is_dir)
        self.__watcher.Add(location)

    def listdir(self, is_absolute: bool = False) -> list:
        files = os.listdir(self.GetPath())
        return files if not is_absolute else [self.GetPath() + file for file in files]

    def get_absolute_path(self, file: str) -> str:
        return self.GetPath() + file if file in self.listdir() else ''

    #TODO при большом количестве файлов удаление происходит медленно, нужно продумать индикацию
    def delete_file(self, filepath: str) -> None:
        if self.is_dir(filepath):
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
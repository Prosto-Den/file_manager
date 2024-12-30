import os
import pathlib as pl
import wx


class FileManipulator(wx.FileSystem):
    def __init__(self,  filepath: str):
        super().__init__()

        if filepath is None:
            filepath = os.path.dirname(__file__)

        self.ChangePathTo(filepath, True)

    def change_path_to(self, location: str, is_dir: bool) -> None:
        self.ChangePathTo(location, is_dir)

    def listdir(self, is_absolute: bool = False) -> list:
        files = os.listdir(self.GetPath())

        if not is_absolute:
            return files
        else:
            return [self.GetPath() + file for file in files]

    def get_absolute_path(self, file: str) -> str:
        return self.GetPath() + file if file in self.listdir() else ''

    @classmethod
    def open_file(cls, filepath: str) -> None:
        os.startfile(filepath)

    @classmethod
    def is_dir(cls, filepath: str) -> bool:
        return pl.Path(filepath).is_dir()

    @classmethod
    def is_file(cls, filepath: str) -> bool:
        return pl.Path(filepath).is_file()

    @classmethod
    def delete_file(cls, filepath: str) -> bool:
        if cls.is_dir(filepath):
            os.rmdir(filepath)
        else:
            os.remove(filepath)

        return True
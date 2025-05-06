from framework.utils.file_utils import FileUtils
from framework.events.events import PathChangedEvent
from framework.utils.time_utils import TimeUtils
import datetime as dt
import string
import wx
import os
import re


class FileSystem(wx.FileSystem):
    def __init__(self, parent: wx.Window, filepath: str) -> None:
        super().__init__()

        filepath = os.path.dirname(filepath)

        self.ChangePathTo(filepath, True)

        #TODO возможно стоит сделать класс связку
        self.__event_handler = parent.EventHandler

        # наблюдатель нужен для отслеживания изменений в файловой системе (удаление/переименование файлов и т.п.)
        # на изменение директории не реагирует
        self.__watcher = wx.FileSystemWatcher()
        self.__watcher.Add(filepath)

    @property
    def watcher(self) -> wx.FileSystemWatcher:
        return self.__watcher

    def change_path_to(self, location: str) -> None:
        """
        Меняет текущую директорию манипулятора
        :param location: Путь к новой директории
        :return:
        """
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
        return files if not is_absolute else [os.path.join(self.GetPath(), file) for file in files]

    def listdir_with_info(self, is_absolute: bool = False) -> list[tuple[str, int, dt.datetime]]:
        """
        Возвращает список с названиями файлов вместе с дополнительной информацией о них (размер файла + дата последнего
        изменения). Для папок размер всегда 0.
        :param is_absolute: Если True - возвращает список с абсолютными путями к файлам. По умолчанию False.
        :return: Список с названиями файлов вместе с их размерами и датами последнего изменения
        """
        files = self.listdir(is_absolute)
        absolute_file_path = self.listdir(True)
        file_info = [FileUtils.get_file_info(file) for file in absolute_file_path]
        sizes = [info.st_size if FileUtils.is_file(file)
                              else 0 for file, info in zip(absolute_file_path, file_info)]
        dates = [TimeUtils.ns_to_datetime(info.st_ctime_ns) for info in file_info]

        return list(zip(files, sizes, dates))

    def get_absolute_path(self, file: str) -> str:
        """
        Вернёт абсолютный путь к файлу, если он есть в директории, куда указывает file manipulator,
        иначе вернёт пустую строку.
        :param file: Название файла
        :return: абсолютный путь к файлу или пустая строка
        """
        return os.path.join(self.GetPath(), file) if file in self.listdir() else ''

    #TODO пока не готово
    def get_checksums(self) -> dict[str, str]:
        """
        Получить контрольные суммы для всех файлов в директории и поддиректориях
        :return: ???
        """
        pass

    def create_folder(self) -> None:
        """
        Создаёт папку в директории, на которую указывает манипулятор
        """
        files = [file for file in self.listdir() if re.match(r'Новая\sпапка\s?\d?', file)]
        filepath = self.GetPath()
        if (length := len(files)) == 0:
            filepath = os.path.join(filepath, 'Новая папка')
        else:
            filepath = os.path.join(filepath, f'Новая папка {length}')
        os.mkdir(filepath)

    def create_file(self, file_format_code: str) -> None:
        """
        Создаёт файл в директории, на которую указывает манипулятор с заданным расширением
        :param file_format_code: Расширение файла
        """
        files = [file for file in self.listdir() if re.match(rf'Документ\s?\d?{file_format_code}', file)]
        filepath = self.GetPath()

        if (length := len(files)) == 0:
            filepath = os.path.join(filepath, ''.join(('Документ', file_format_code)))
        else:
            filepath = os.path.join(filepath, ''.join((f'Документ {length}', file_format_code)))

        file = open(filepath, 'w')
        file.close()

    def get_total_file_amount(self) -> int:
        """
        Рекурсивно вычисляет количество файлов в директории и поддиректориях
        :return: Количество файлов
        """
        result = 0

        for _, _, files in os.walk(self.GetPath()):
            result += len(files)

        return result

    @staticmethod
    def get_logical_drives() -> list[str]:
        return ['{}:/'.format(d) for d in string.ascii_uppercase if os.path.exists('{}:'.format(d))]

    @staticmethod
    def copy_to_clipboard(filepath: str) -> None:
        clipboard: wx.Clipboard = wx.Clipboard.Get()

        if clipboard.Open():
            clipboard.SetData(wx.TextDataObject(filepath))
            clipboard.Close()

    @staticmethod
    def get_data_from_clipboard() -> list[str]:
        clipboard: wx.Clipboard = wx.Clipboard.Get()
        data = wx.TextDataObject()
        files = ''

        if clipboard.Open():
            clipboard.GetData(data)
            files = data.GetText()
            clipboard.Close()

        return files.split(r'\?\\')
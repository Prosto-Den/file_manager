from framework.utils.file_utils import FileUtils
from framework.utils.time_utils import TimeUtils
from framework.events import PathChanged
import datetime as dt
import string
import wx
import os
import re


#TODO дописать документацию
class FileSystem(wx.FileSystem):
    def __init__(self, parent: wx.Window, filepath: str) -> None:
        super().__init__()
        self.__parent = parent

        if FileUtils.is_file(filepath):
            filepath = os.path.dirname(filepath)

        self.ChangePathTo(filepath, True)

        # наблюдатель нужен для отслеживания изменений в файловой системе (удаление/переименование файлов и т.п.)
        # на изменение директории не реагирует
        self.__watcher = wx.FileSystemWatcher()
        self.__watcher.Add(filepath)


    @property
    def watcher(self) -> wx.FileSystemWatcher:
        """
        Наблюдатель отслеживает изменения в файловой системе
        :return: wx.FileSystemWatcher
        """
        return self.__watcher

    def change_path_to(self, location: str) -> None:
        """
        Меняет текущую директорию системы
        :param location: Путь к новой директории
        """
        self.__watcher.RemoveAll()
        self.ChangePathTo(location, True)
        self.__watcher.Add(location)

        event = PathChanged()
        wx.PostEvent(self.__parent.GetEventHandler(), event)

    @classmethod
    def listdir(cls, path: str, is_absolute: bool = False) -> list[str]:
        """
        Возвращает список с названиями файлов, которые расположены в директории
        :param path: Путь к директории
        :param is_absolute: Если True - возвращает список с абсолютными путями к файлам. По умолчанию False.
        :return: Список с названиями файлов
        """
        files = os.listdir(path)
        return files if not is_absolute else [cls.path_join(path, file) for file in files]

    @classmethod
    def listdir_with_info(cls, path: str, is_absolute: bool = False) -> list[tuple[str, int, dt.datetime]]:
        """
        Возвращает список с названиями файлов вместе с дополнительной информацией о них (размер файла + дата последнего
        изменения). Для директорий размер всегда 0.
        :param path: Путь к директории
        :param is_absolute: Если True - возвращает список с абсолютными путями к файлам. По умолчанию False.
        :return: Список с названиями файлов вместе с их размерами и датами последнего изменения
        """
        files = cls.listdir(path, is_absolute)
        absolute_file_path = cls.listdir(path, True)
        file_info = [FileUtils.get_file_info(file) for file in absolute_file_path]
        sizes = [info.st_size if FileUtils.is_file(file)
                              else 0 for file, info in zip(absolute_file_path, file_info)]
        dates = [TimeUtils.ns_to_datetime(info.st_mtime_ns) for info in file_info]

        return list(zip(files, sizes, dates))

    @classmethod
    def get_absolute_path(cls, path: str, file: str) -> str:
        """
        Вернёт абсолютный путь к файлу, если он есть в директории, иначе вернёт пустую строку.
        :param path: Путь к директории
        :param file: Название файла
        :return: абсолютный путь к файлу или пустая строка
        """
        return cls.path_join(path, file) if file in cls.listdir(path) else ''

    #TODO добавить параметр folder_name, который будем брать из настроек, а тут уже форматировать как надо
    @classmethod
    def create_folder(cls, path: str) -> None:
        """
        Создаёт папку в директории, на которую указывает манипулятор
        :param path:
        """
        files = [file for file in cls.listdir(path) if re.match(r'Новая\sпапка\s?\d?', file)]
        if (length := len(files)) == 0:
            path = cls.path_join(path, 'Новая папка')
        else:
            path = cls.path_join(path, f'Новая папка {length}')
        os.mkdir(path)

    #TODO добавить параметр file_name, который будем брать из настроек, а тут уже форматировать как надо
    @classmethod
    def create_file(cls, path: str, file_format_code: str) -> None:
        """
        Создаёт файл в директории, на которую указывает манипулятор с заданным расширением
        :param path:
        :param file_format_code: Расширение файла
        """
        files = [file for file in cls.listdir(path) if re.match(rf'Документ\s?\d?{file_format_code}', file)]

        if (length := len(files)) == 0:
            path = cls.path_join(path, ''.join(('Документ', file_format_code)))
        else:
            path = cls.path_join(path, ''.join((f'Документ {length}', file_format_code)))

        file = open(path, 'w')
        file.close()

    #TODO нужен ли этот метод?
    @staticmethod
    def get_total_file_amount(path: str) -> int:
        """
        Рекурсивно вычисляет количество файлов в директории и поддиректориях
        :param path:
        :return: Количество файлов
        """
        result = 0

        for _, _, files in os.walk(path):
            result += len(files)

        return result

    @staticmethod
    def get_logical_drives() -> list[str]:
        """
        Возвращает все диски буквенные обозначения для информационных носителей.
        Актуально только для Windows
        :return:
        """
        return ['{}:/'.format(d) for d in string.ascii_uppercase if os.path.exists('{}:'.format(d))]

    #TODO кринжовая функция
    @staticmethod
    def copy_to_clipboard(filepath: str) -> None:
        clipboard: wx.Clipboard = wx.Clipboard.Get()

        if clipboard.Open():
            clipboard.SetData(wx.TextDataObject(filepath))
            clipboard.Close()

    #TODO заменить все использования этого метода аналогичным из PathHelper
    @staticmethod
    def path_join(*args: str) -> str:
        root, *other = args
        path = os.path.join(root, *other)
        return path.replace('\\', '/')

    @classmethod
    def is_clipboard_empty(cls) -> bool:
        files = cls.get_data_from_clipboard()
        return not all([os.path.exists(file) for file in files])

    #TODO заменить разделитель
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

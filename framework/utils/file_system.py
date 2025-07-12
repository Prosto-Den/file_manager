from framework.utils.file_utils import FileUtils
from framework.utils.time_utils import TimeUtils
from framework.events import PathChanged
from framework.utils.path_helper import PathHelper
import datetime as dt
import string
import wx
import os
import re
import platform
from pathlib import Path


#TODO дописать документацию
#TODO может быть всё взаимодействие с файловой системой стоит перенести на Java
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
        Наблюдатель.  Нужен для отслеживания изменений в файловой системе (удаление/переименование файлов и т.п.)
        На изменение директории не реагирует.
        :return: Наблюдатель (FileSystemWatcher)
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

        # сообщаем родителю об изменении директории
        event = PathChanged()
        wx.PostEvent(self.__parent.GetEventHandler(), event)

    @staticmethod
    def listdir(path: str, is_absolute: bool = False) -> list[str]:
        """
        Возвращает список с названиями файлов, которые расположены в директории
        :param path: Путь к директории
        :param is_absolute: Если True - возвращает список с абсолютными путями к файлам. По умолчанию False.
        :return: Список с названиями файлов
        """
        files = os.listdir(path)
        return files if not is_absolute else [PathHelper.join(path, file) for file in files]

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

    #TODO нигде не используется, возможно не нужен
    @classmethod
    def get_absolute_path(cls, path: str, file: str) -> str:
        """
        Вернёт абсолютный путь к файлу, если он есть в директории, иначе вернёт пустую строку.
        :param path: Путь к директории
        :param file: Название файла
        :return: абсолютный путь к файлу или пустая строка
        """
        return PathHelper.join(path, file) if file in cls.listdir(path) else ''

    #TODO придумать, как это дело локализовать
    @classmethod
    def create_folder(cls, path: str, folder_name: str) -> None:
        """
        Создаёт папку в директории
        :param path: Путь к директории, в которой будет создана папка
        :param folder_name: Название папки
        """
        re_expression = cls.__create_re_expression(folder_name)
        files = [file for file in cls.listdir(path) if re.match(re_expression, file)]
        if (length := len(files)) == 0:
            path = PathHelper.join(path, folder_name)
        else:
            path = PathHelper.join(path, ''.join((folder_name, ' ', str(length))))
        os.mkdir(path)

    @classmethod
    def create_file(cls, path: str, filename: str) -> None:
        """
        Создаёт файл в директории
        :param path: Полный путь к директории, где будет создан файл
        :param filename: Название файла
        """
        filepath = Path(filename)
        name = str(filepath.with_suffix(''))
        suffix = filepath.suffix
        re_expression = cls.__create_re_expression(filename)
        files = [file for file in cls.listdir(path) if re.match(re_expression, file)]

        if (length := len(files)) == 0:
            path = PathHelper.join(path, filename)
        else:
            path = PathHelper.join(path, ''.join((name, ' ', str(length), suffix)))

        file = open(path, 'w')
        file.close()

    @staticmethod
    def get_logical_drives() -> tuple[str, ...]:
        """
        Возвращает буквенные обозначения для информационных носителей.
        Актуально только для Windows
        :return:
        """
        return tuple(['{}:/'.format(d) for d in string.ascii_uppercase if os.path.exists('{}:'.format(d))])

    #TODO надо посмотреть, как нормально работать с буфером обмена
    @staticmethod
    def copy_to_clipboard(filepath: str) -> None:
        clipboard: wx.Clipboard = wx.Clipboard.Get()

        if clipboard.Open():
            clipboard.SetData(wx.TextDataObject(filepath))
            clipboard.Close()

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

    @staticmethod
    def is_root_dir(current_path: str) -> bool:
        """
        Проверяет, является ли указанный путь корнем системы
        :param current_path: Путь для проверки
        :return: True, если путь является корнем системы (например, "C:/" для Windows, "/" для Linux),
                иначе False
        """
        if platform.system() == 'Windows':
            return not (re.match(r'\w:/\b', current_path) or re.match(r"\w:/\W", current_path))
        else:
            return not (re.match(r'/\b', current_path) or re.match(r"\w:/\W", current_path))

    @staticmethod
    def __create_re_expression(filename: str) -> str:
        path = Path(filename)
        suffix = path.suffix
        name = str(path.with_suffix(''))
        result = name.replace(' ', r'\s?')
        return ''.join((result, r'\s?.?\d?.?', suffix))

    @staticmethod
    def is_exists(path: str) -> bool:
        return os.path.exists(path)

    @staticmethod
    def get_root_directory() -> str:
        return "C:/" if platform.system() == 'Windows' else '/'

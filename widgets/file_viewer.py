from __future__ import annotations
from typing import TYPE_CHECKING, override
from settings.consts import FILE_VIEWER_STYLE
from windows.popup_menu import PopUpMenu
from framework.observer.observable import Observable
from framework.utils import FileUtils
from framework.utils.file_system import FileSystem
from settings.icon_manipulators import IconManipulators
from framework.events import EVT_PATH_CHANGED, AddFileToHistoryEvent
from settings.consts import POPUP_MENU_SIZE
from settings.enums import FileViewerIconID, FileViewerColumns, SortFlags, IconManipulatorID
from app_manager import AppManager
import datetime as dt
from framework.utils.path_helper import PathHelper
import wx
import os


if TYPE_CHECKING:
    from widgets.main_panel import MainPanel


class FileViewer(wx.ListCtrl, Observable):
    def __init__(self, parent: MainPanel, id: int = wx.ID_ANY,
                 style: int = FILE_VIEWER_STYLE, pos: wx.Point = wx.DefaultPosition,
                 validator: wx.Validator = wx.DefaultValidator, name: str = wx.ListCtrlNameStr) -> None:
        super(wx.ListCtrl, self).__init__(parent=parent, id=id, style=style, validator=validator, name=name, pos=pos)
        Observable.__init__(self)

        self.SetSize(parent.GetSize())

        # подключаем иконки
        file_viewer_icons = IconManipulators.get_icon_manipulator(IconManipulatorID.FILE_VIEWER)
        self.SetImageList(file_viewer_icons, wx.IMAGE_LIST_SMALL)

        self.__file_system = FileSystem(self, __file__)
        #TODO флаг сортировки переместить в настройки
        self.__sort_flag = SortFlags.BY_NAME

        # обновляем наполнение виджета
        self.update()

        # подключаемся к событиям
        # EVT_PATH_CHANGED - кастомное событие. Сообщает о смене директории
        self.Bind(event=EVT_PATH_CHANGED, handler=lambda _: self.update())
        # wx.EVT_FSWATCHER - событие от наблюдателя. Срабатывает, если произошло создание/удаление/переименование
        # файла
        self.__file_system.watcher.Bind(wx.EVT_FSWATCHER, lambda _: self.update())
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, lambda _: self.__open())
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, handler=self.__summon_popup_menu)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.__change_sort_flag)

    @override
    def notify(self, filepath: str) -> None:
        for observer in self._observers:
            observer.update(filepath)

    @property
    def file_system(self) -> FileSystem:
        """
        Файловый манипулятор виджета
        :return: Файловый манипулятор
        """
        return self.__file_system

    def update(self) -> None:
        """
        Обновляет содержимое обозревателя файлов
        """
        # очищаем всё содержимое виджета
        self.Freeze()
        self.ClearAll()

        current_path = self.__file_system.GetPath()
        # Создаём колонки для виджета. Если текущее положение не в корневой папке,
        # то добавляем кнопку подъёма по директории
        self.__create_columns()
        if not FileSystem.is_root_dir(current_path):
            self.InsertItem(0, '..', FileViewerIconID.BACK_ICON)

        if not os.access(current_path, os.R_OK):
            # Здесь по идее должен быть запрос на повышение привилегий (elevate)
            wx.MessageBox(AppManager.Translation.access_denied_text,
                          AppManager.Translation.access_denied_title)
            self.Thaw()
            return

        # Получаем файлы текущей директории. Сортируем их согласно флагу
        files = self.__file_system.listdir_with_info(current_path)
        self.__sort(files)

        # заполняем виджет
        index: int; file: str; size: int; date: dt.datetime
        for index, (file, size, date) in enumerate(files, start=1):
            # определяем абсолютный путь до файла
            path = PathHelper.join(current_path, file)
            is_directory: bool = FileUtils.is_dir(path)
            icon_id = FileViewerIconID.FOLDER_ICON if is_directory else FileViewerIconID.FILE_ICON
            # переводим размер файла из байтов в КБ, МБ и прочее
            size_as_bytes = FileUtils.convert_bytes(size) if not is_directory else ''

            item_index = self.InsertItem(index, file, icon_id)
            #TODO можно сделать побольше колонок
             # выставляем информацию для колонок
            self.SetItem(item_index, 1, str(size_as_bytes))
            self.SetItem(item_index, 2, date.strftime(AppManager.Settings.Instance.time_format))

        # сообщаем подписчикам об обновлении
        self.notify(current_path)

        # размораживаем виджет
        self.Thaw()

    #TODO создать класс конфигурации, в котором будем хранить положения столбцов
    def __create_columns(self) -> None:
        """
        Создать колонки для виджета
        """
        self.AppendColumn(AppManager.Translation.filename_column)
        self.AppendColumn(AppManager.Translation.file_size_column)
        self.AppendColumn(AppManager.Translation.change_date_column)
        self.__set_default_column_width()

    def __set_default_column_width(self) -> None:
        """
        Установить ширину колонок по умолчанию
        """
        column_amount = self.GetColumnCount()
        column_width = self.GetSize().GetWidth() // column_amount

        for column in range(column_amount):
            self.SetColumnWidth(column, column_width)

    def __summon_popup_menu(self, event: wx.ListEvent) -> None:
        """
        Вызвать контекстное меня при нажатии ПКМ по элементу списка
        :param event: Связанное со списком событие
        """
        if event.GetText() != '..':
            popup = PopUpMenu(self, event)
            popup.set_filepath(self.__file_system.GetPath())
            popup.set_position(self.ClientToScreen(event.GetPoint()))
            popup.set_size(POPUP_MENU_SIZE)
            popup.Show(True)

    def __open(self) -> None:
        """
        Открыть файл/перейти в директорию
        """
        item_label = self.GetItemText(self.GetFirstSelected())

        if item_label == '..':
            filepath: str = self.__file_system.GetPath()
            filename_lst: list = filepath.split('/')
            filename_lst.pop(-2)
            filepath = '/'.join(filename_lst)
        else:
            filepath: str = self.__file_system.GetPath() +  item_label

        if not FileUtils.is_dir(filepath):
            FileUtils.open_file(filepath)
        else:
            parent: MainPanel = self.GetParent()
            event = AddFileToHistoryEvent(filepath=self.__file_system.GetPath())
            wx.PostEvent(parent.GetEventHandler(), event)
            self.__file_system.change_path_to(filepath)
            self.update()

    #TODO наверное, надо вынести куда-то. Всё-таки это не задача FileViewer'а
    def __change_sort_flag(self, event: wx.ListEvent) -> None:
        """
        Изменить значение флага сортировки
        :param event: Связанное со списком событие
        :return:
        """
        match event.GetColumn():
            case FileViewerColumns.NAME:
                self.__sort_flag = SortFlags.BY_NAME_DESCENDING if self.__sort_flag == SortFlags.BY_NAME \
                                                                else self.__sort_flag.BY_NAME
            case FileViewerColumns.SIZE:
                self.__sort_flag = SortFlags.BY_SIZE_DESCENDING if self.__sort_flag == SortFlags.BY_SIZE \
                                                                else self.__sort_flag.BY_SIZE
            case FileViewerColumns.CHANGE_DATE:
                self.__sort_flag = SortFlags.BY_DATE_DESCENDING if self.__sort_flag == SortFlags.BY_DATE \
                                                                else self.__sort_flag.BY_DATE

        # сразу же обновляем виджет, чтобы применить сортировку
        self.update()

    #TODO наверное, надо вынести куда-то. Всё-таки это не задача FileViewer'а
    def __sort(self, files: list[tuple[str, int, dt.datetime]]) -> None:
        """
        Отсортировать файлы из директории
        :param files: Файлы директории
        """
        match self.__sort_flag:
            case SortFlags.BY_NAME:
                files.sort(key=lambda item: item[0])
            case SortFlags.BY_NAME_DESCENDING:
                files.sort(key=lambda item: item[0], reverse=True)
            case SortFlags.BY_SIZE:
                files.sort(key=lambda item: item[1])
            case SortFlags.BY_SIZE_DESCENDING:
                files.sort(key=lambda item: item[1], reverse=True)
            case SortFlags.BY_DATE:
                files.sort(key=lambda item: item[2])
            case SortFlags.BY_DATE_DESCENDING:
                files.sort(key=lambda item: item[2], reverse=True)

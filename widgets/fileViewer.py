import wx
import re
from settings.consts import FILE_VIEWER_STYLE
from windows.popupmenu import PopUpMenu
from framework.utils import FileManipulator
from framework.events import EVT_PATH_CHANGED
from settings.consts import POPUP_MENU_SIZE, TIME_FORMAT
from settings.enums import FileViewerIconID, FileViewerColumns, SortFlags
from widgets.controlPanel import ControlPanel
from framework.utils.fileSize import FileSize
import datetime as dt


class FileViewer(wx.ListCtrl):
    def __init__(self, parent: wx.Window, filepath: str, control_panel: ControlPanel, id: int = wx.ID_ANY,
                 style: int = FILE_VIEWER_STYLE, pos: wx.Point = wx.DefaultPosition,
                 validator: wx.Validator = wx.DefaultValidator, name: str = wx.ListCtrlNameStr) -> None:
        wx.ListCtrl.__init__(self, parent=parent, id=id, style=style, validator=validator, name=name, pos=pos)

        self.SetSize(parent.GetSize())

        self.__file_system = FileManipulator(filepath, self.GetEventHandler())
        self.__related_control_panel: ControlPanel = control_panel
        self.__sort_flag = SortFlags.BY_NAME

        self.Bind(event=EVT_PATH_CHANGED, handler=lambda _: self.__update())
        self.__file_system.watcher.Bind(wx.EVT_FSWATCHER, lambda _: self.__update())
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, lambda _: self.__open())
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, handler=self.__summon_popup_menu)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.__do_sort)

        self.__update()

    @property
    def file_system(self) -> FileManipulator:
        return self.__file_system

    def __create_columns(self) -> None:
        self.AppendColumn('Имя файла')
        self.AppendColumn('Размер файла')
        self.AppendColumn('Дата изменения')
        self.__set_default_column_width()

    def __get_items_from_column(self, column: int) -> list[str]:
        return [self.GetItemText(index, column) for index in range(1, len(self.__file_system.listdir()))]

    def __set_default_column_width(self) -> None:
        column_amount = self.GetColumnCount()
        column_width = self.GetSize().GetWidth() // column_amount

        for column in range(column_amount):
            self.SetColumnWidth(column, column_width)

    def __update(self) -> None:
        self.ClearAll()

        current_path = self.__file_system.GetPath()
        self.__related_control_panel.set_filepath(current_path)

        self.__create_columns()
        if re.match(r'\w:/\b', current_path):
            self.InsertItem(0, '..', FileViewerIconID.BACK_ICON)

        files = self.__file_system.listdir_with_info()
        self.__sort(files)

        index: int; file: str; size: int; date: dt.datetime
        for index, (file, size, date) in enumerate(files, start=1):
            is_directory: bool = self.__file_system.is_dir(self.__file_system.GetPath() + file)
            icon_id = FileViewerIconID.FOLDER_ICON if is_directory else FileViewerIconID.FILE_ICON
            item_index = self.InsertItem(index, file, icon_id)
            size_as_bytes = FileSize(self.__file_system.convert_bytes(size))
            self.SetItem(item_index, 1, str(size_as_bytes))
            self.SetItem(item_index, 2, date.strftime(TIME_FORMAT))

    def __summon_popup_menu(self, event: wx.ListEvent) -> None:
        if event.GetText() != '..':
            popup = PopUpMenu(self, self.__file_system.GetPath(), event)
            popup.set_position(self.ClientToScreen(event.GetPoint()))
            popup.set_size(POPUP_MENU_SIZE)
            popup.Show(True)

    def __open(self) -> None:
        item_label = self.GetItemText(self.GetFirstSelected())

        if item_label == '..':
            filename: str = self.__file_system.GetPath()
            filename_lst: list = filename.split('/')
            filename_lst.pop(-2)
            filename = '/'.join(filename_lst)
        else:
            filename: str = self.__file_system.GetPath() +  item_label

        if not self.__file_system.is_dir(filename):
            self.__file_system.open_file(filename)
        else:
            self.__file_system.change_path_to(filename, True)
            self.__update()

    def __do_sort(self, event: wx.ListEvent) -> None:
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

        self.__update()

    def __sort(self, files: list[tuple[str, int, dt.datetime]]) -> None:
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
import wx
import re
from settings.consts import FILE_VIEWER_STYLE
from windows.popupmenu import PopUpMenu
from framework.utils import FileManipulator
from framework.utils.timeFunc import ns_to_datetime_as_string
from framework.events import EVT_PATH_CHANGED
from settings.consts import POPUP_MENU_SIZE, TIME_FORMAT
from settings.enums import FileViewerIconID, FileViewerColumns
from widgets.controlPanel import ControlPanel


class FileViewer(wx.ListCtrl):
    def __init__(self, parent: wx.Window, filepath: str, control_panel: ControlPanel, id: int = wx.ID_ANY,
                 style: int = FILE_VIEWER_STYLE, pos: wx.Point = wx.DefaultPosition,
                 validator: wx.Validator = wx.DefaultValidator, name: str = wx.ListCtrlNameStr) -> None:
        wx.ListCtrl.__init__(self, parent=parent, id=id, style=style, validator=validator, name=name, pos=pos)
        self.SetSize(parent.GetSize())

        self.__file_system = FileManipulator(filepath, self.GetEventHandler())
        self.__related_control_panel: ControlPanel = control_panel

        self.Bind(event=EVT_PATH_CHANGED, handler=lambda _: self.__update())
        self.__file_system.watcher.Bind(wx.EVT_FSWATCHER, lambda _: self.__update())
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, handler=lambda _: self.__open())
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, handler=self.__summon_popup_menu)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.__sort)

        self.__update()

    @property
    def file_system(self) -> FileManipulator:
        return self.__file_system

    def __create_columns(self) -> None:
        self.AppendColumn('Имя файла', width=self.GetSize().GetWidth() // 3)
        self.AppendColumn('Размер файла', width=self.GetSize().GetWidth() // 3)
        self.AppendColumn('Дата изменения', width=self.GetSize().GetWidth() // 3)

    def __update(self) -> None:
        self.ClearAll()

        current_path = self.__file_system.GetPath()
        self.__related_control_panel.set_filepath(current_path)

        self.__create_columns()
        if re.match(r'\w:/\b', current_path):
            self.InsertItem(0, '..', FileViewerIconID.BACK_ICON)

        files = self.__file_system.listdir()
        for index, file in enumerate(files, start=1):
            is_directory: bool = self.__file_system.is_dir(self.__file_system.GetPath() + file)
            icon_id = FileViewerIconID.FOLDER_ICON if is_directory else FileViewerIconID.FILE_ICON
            item_index = self.InsertItem(index, file, icon_id)
            absolute_path = self.__file_system.get_absolute_path(file)
            size_label = '' if self.__file_system.is_dir(absolute_path) \
                            else FileManipulator.convert_bytes(self.__file_system.get_file_info(absolute_path).st_size)
            date_label = ns_to_datetime_as_string(self.__file_system.get_file_info(absolute_path).st_ctime_ns, TIME_FORMAT)
            self.SetItem(item_index, 1, size_label)
            self.SetItem(item_index, 2, date_label)

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

    def __sort(self, event: wx.ListEvent) -> None:
        match event.GetColumn():
            case FileViewerColumns.NAME:
                pass
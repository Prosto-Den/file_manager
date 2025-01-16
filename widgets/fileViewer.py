import wx
import re
from settings.consts import FILE_VIEWER_STYLE
from windows.popupmenu import PopUpMenu
from framework.utils import FileManipulator
from framework.events import EVT_PATH_CHANGED
from settings.consts import POPUP_MENU_SIZE
from settings.enums import FileViewerIconID, WidgetID


class FileViewer(wx.ListCtrl):
    def __init__(self, parent: wx.Window, id: int = wx.ID_ANY,
                 style: int = FILE_VIEWER_STYLE,
                 validator: wx.Validator = wx.DefaultValidator, name: str = wx.ListCtrlNameStr,
                 filepath: str = None) -> None:
        super().__init__(parent=parent, id=id, style=style, validator=validator, name=name)
        self.SetSize(parent.GetSize())

        if filepath is None:
            control_panel_id = WidgetID.LEFT_CONTROL_PANEL if self.GetId() == WidgetID.LEFT_FILE_VIEWER \
                                                           else WidgetID.RIGHT_CONTROL_PANEL
            control_panel = self.FindWindowById(control_panel_id)
            filepath = control_panel.disk

        self.__file_system = FileManipulator(filepath, self.GetEventHandler())
        self.Bind(event=EVT_PATH_CHANGED, handler=lambda _: self.__update())
        self.__file_system.watcher.Bind(wx.EVT_FSWATCHER, lambda _: self.__update())
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, handler=lambda _: self.__open())
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, handler=self.__summon_popup_menu)

        self.__update()

    @property
    def file_system(self) -> FileManipulator:
        return self.__file_system

    def __update(self) -> None:
        self.ClearAll()

        current_path = self.__file_system.GetPath()
        self.AppendColumn(current_path, width=self.GetSize().GetWidth())
        if re.match(r'\w:/\b', current_path):
            self.InsertItem(0, '..', FileViewerIconID.BACK_ICON)

        files = self.__file_system.listdir()
        for index, file in enumerate(files, start=1):
            is_directory: bool = self.__file_system.is_dir(self.__file_system.GetPath() + file)
            icon_id = FileViewerIconID.FOLDER_ICON if is_directory else FileViewerIconID.FILE_ICON
            self.InsertItem(index, file, icon_id)

    def __summon_popup_menu(self, event: wx.ListEvent) -> None:
        if event.GetText() != '..':
            popup = PopUpMenu(self, self.__file_system.GetPath() + event.GetText(), event)
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
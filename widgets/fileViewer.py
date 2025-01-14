import wx
import re
from settings import consts
from windows.popupmenu import PopUpMenu
from framework.utils import FileManipulator
from settings.consts import POPUP_MENU_SIZE
from settings.enums import FileViewerIconID


class FileViewer(wx.ListCtrl):
    def __init__(self, parent: wx.Window, id: int = wx.ID_ANY, pos: wx.Point = wx.DefaultPosition,
                 size: wx.Size = wx.DefaultSize, style: int = consts.FILE_VIEWER_STYLE,
                 validator: wx.Validator = wx.DefaultValidator, name: str = wx.ListCtrlNameStr,
                 filepath: str = None) -> None:
        super().__init__(parent=parent, id=id, pos=pos, size=size, style=style, validator=validator, name=name)
        self.SetSize(parent.GetSize())

        self.__file_system = FileManipulator(filepath)
        self.__file_system.watcher.Bind(wx.EVT_FSWATCHER, lambda _: self.update())

        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, handler=lambda _: self.__open())
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, handler=self.__summon_popup_menu)
        self.update()

    @property
    def file_system(self) -> FileManipulator:
        return self.__file_system

    def update(self) -> None:
        self.ClearAll()

        current_path = self.__file_system.GetPath()
        self.AppendColumn(current_path, width=self.GetSize().GetWidth())
        if re.match(r'\w:/\b', current_path):
            self.InsertItem(0, '..', FileViewerIconID.FOLDER_ICON)

        files = self.__file_system.listdir()
        for index, file in enumerate(files, start=1):
            is_directory: bool = self.__file_system.is_dir(self.__file_system.GetPath() + file)
            icon_id = FileViewerIconID.FOLDER_ICON if is_directory else FileViewerIconID.FILE_ICON
            self.InsertItem(index, file, icon_id)

    def __summon_popup_menu(self, event: wx.ListEvent) -> None:
        if event.GetText() != '..':
            PopUpMenu.init(self, self.__file_system.GetPath() + event.GetText(), event)
            PopUpMenu.set_position(self.ClientToScreen(event.GetPoint()))
            PopUpMenu.set_size(POPUP_MENU_SIZE)
            PopUpMenu.show()

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
            self.update()
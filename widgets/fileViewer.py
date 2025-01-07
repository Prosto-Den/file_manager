import wx
import re
from settings import consts
from windows.popupmenu import PopUpMenu
from framework.utils import FileManipulator
from settings.consts import POPUP_MENU_SIZE


class FileViewer(wx.ListCtrl):
    def __init__(self, parent: wx.Window, id: int = wx.ID_ANY, pos: wx.Point = wx.DefaultPosition,
                 size: wx.Size = wx.DefaultSize, style: int = consts.FILE_VIEWER_STYLE,
                 validator: wx.Validator = wx.DefaultValidator, name: str = wx.ListCtrlNameStr,
                 filepath: str = None) -> None:
        super().__init__(parent=parent, id=id, pos=pos, size=size, style=style, validator=validator, name=name)

        self.__file_system = FileManipulator(filepath)
        self.__file_system.watcher.Bind(wx.EVT_FSWATCHER, lambda _: self.update())
        self.update()

        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, handler=lambda _: self.__open())
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, handler=self.__summon_popup_menu)

    @property
    def file_system(self) -> FileManipulator:
        return self.__file_system

    def update(self) -> None:
        self.ClearAll()

        current_path = self.__file_system.GetPath()
        self.AppendColumn(current_path, width=540)
        if re.match(r'\w:/\b', current_path):
            self.InsertItem(0, '..', 0)

        files = self.__file_system.listdir()
        for index, file in enumerate(files, start=1):
            is_directory: bool = not self.__file_system.is_dir(self.__file_system.GetPath() + file)
            self.InsertItem(index, file, is_directory)

    def __summon_popup_menu(self, event: wx.ListEvent) -> None:
        PopUpMenu.init(self, self.__file_system.GetPath() + event.GetText(), event)
        PopUpMenu.set_position(self.ClientToScreen(event.GetPoint()))
        PopUpMenu.set_size(wx.Size(*POPUP_MENU_SIZE))
        PopUpMenu.show()

    def __test(self, event) -> None:
        print(event)

    def __open(self) -> None:
        item_label = self.GetItemText(self.GetFirstSelected())

        if item_label == '..':
            filename: str = self.__file_system.GetPath()
            filename_lst: list = filename.split('/')
            filename_lst.pop(-2)
            filename = '/'.join(filename_lst)
        else:
            filename: str = self.__file_system.GetPath() + item_label

        if not self.__file_system.is_dir(filename):
            self.__file_system.open_file(filename)
        else:
            self.__file_system.change_path_to(filename, True)
            self.update()
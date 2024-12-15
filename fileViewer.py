import wx
import os
import pathlib


class FileViewer(wx.ListCtrl):
    def __init__(self, parent: wx.Window, id: int = wx.ID_ANY, pos: wx.Point = wx.DefaultPosition,
                 size: wx.Size = wx.DefaultSize, style: int = wx.LC_REPORT | wx.LC_HRULES | wx.LC_EDIT_LABELS,
                 validator: wx.Validator = wx.DefaultValidator, name: str = wx.ListCtrlNameStr) -> None:
        super().__init__(parent=parent, id=id, pos=pos, size=size, style=style, validator=validator, name=name)

        self.__file_system = wx.FileSystem()
        self.__file_system.ChangePathTo(os.path.dirname(__file__), True)
        self.__fill()
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, handler=lambda _: self.open())

    def __fill(self) -> None:
        self.ClearAll()
        self.AppendColumn(self.__file_system.GetPath(), width=540)

        self.InsertItem(0, '..', 0)
        files = os.listdir(self.__file_system.GetPath())
        for index, file in enumerate(files, start=1):
            is_directory = not pathlib.Path(self.__file_system.GetPath() + file).is_dir()
            self.InsertItem(index, file, is_directory)

    def open(self) -> None:
        item_label = self.GetItemText(self.GetFirstSelected())

        if item_label == '..':
            filename: str = self.__file_system.GetPath()
            filename_lst = filename.split('/')
            filename_lst.pop(-2)
            filename = '/'.join(filename_lst)
        else:
            filename: str = self.__file_system.GetPath() + item_label

        if not pathlib.Path(filename).is_dir():
            os.startfile(filename)
        else:
            self.__file_system.ChangePathTo(filename, True)
            self.__fill()

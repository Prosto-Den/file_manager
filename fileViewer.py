import wx
import os
import pathlib


class FileViewer(wx.ListCtrl):
    def __init__(self, parent: wx.Window, id: int = wx.ID_ANY, pos: wx.Point = wx.DefaultPosition,
                 size: wx.Size = wx.DefaultSize, style: int = wx.LC_LIST,
                 validator: wx.Validator = wx.DefaultValidator, name: str = wx.ListCtrlNameStr) -> None:
        super().__init__(parent=parent, id=id, pos=pos, size=size, style=style, validator=validator, name=name)
        self.file_system = wx.FileSystem()
        self.file_system.ChangePathTo(os.path.dirname(__file__), True)
        self.__fill()
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, handler=lambda _: self.open())

    def __fill(self) -> None:
        self.ClearAll()
        files = os.listdir(self.file_system.GetPath())
        self.InsertItem(0, '..', 0)

        for index, file in enumerate(files, start=1):
            is_directory = not pathlib.Path(self.file_system.GetPath() + file).is_dir()
            self.InsertItem(index, file, is_directory)

    def open(self) -> None:
        item_label = self.GetItemText(self.GetFirstSelected())

        if item_label != '..':
            filename: str = self.file_system.FindFirst(item_label, 0)
            filename = filename.replace('file:///', '')
        else:
            filename: str = self.file_system.GetPath() + '..'

        if not pathlib.Path(filename).is_dir():
            os.startfile(filename)
        else:
            self.file_system.ChangePathTo(filename, True)
            self.__fill()

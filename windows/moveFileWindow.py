import wx


class MoveFileWindow(wx.Frame):
    def __init__(self, parent: wx.Window = None, id: int = wx.ID_ANY, size: wx.Size = wx.DefaultSize,
                 pos: wx.Point = wx.DefaultPosition, title: str = 'Title',
                 style=wx.DEFAULT_FRAME_STYLE, name: str = wx.EmptyString):
        super().__init__(parent=parent, id=id, size=size, pos=pos, title=title, style=style, name=name)

        self.__current_file = wx.TextCtrl(parent=self, style=wx.TE_READONLY)
        self.__tre_view = wx.TreeCtrl(parent=self)

        self.Show()

    def __fill_tree_view(self):
        pass
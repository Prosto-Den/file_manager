import wx
from findDuplicateWindow import FindDuplicateWindow
from framework.windows import Window
from settings.enums import ToolID


class MainWindow(Window):
    def __init__(self, parent: wx.Window=None, id: int =wx.ID_ANY, size: wx.Size=wx.Size(1095, 860),
                 pos: wx.Point= wx.DefaultPosition, title='Title', style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER):
        super().__init__(parent=parent, id=id, size=size, pos=pos, title=title, style=style)
        self.toolbar: wx.ToolBar = self.CreateToolBar()

        bitmap = wx.Bitmap(img=wx.Image(name='./icons/toolbar/find_duplicates_icon.ico', type=wx.BITMAP_TYPE_ICO))
        btn: wx.ToolBarToolBase = self.toolbar.CreateTool(toolId=ToolID.FIND_DUPLICATES, label='find',
                                                          bmpNormal=bitmap)
        self.toolbar.Bind(event=wx.EVT_TOOL, handler=self.__find_duplicates, id=ToolID.FIND_DUPLICATES)
        self.toolbar.AddTool(btn)

    def show(self):
        self.Show(True)
        self.toolbar.Realize()

    @staticmethod
    def __find_duplicates(_):
        FindDuplicateWindow()
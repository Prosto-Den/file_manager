from .findDuplicateWindow import FindDuplicateWindow
from framework.windows import Window
from settings.enums import ToolID
from settings.iconManipulators import ToolBarIcons
from settings.consts import MAIN_WINDOW_STYLE
import wx


class MainWindow(Window):
    def __init__(self, *, parent: wx.Window=None, id: int=wx.ID_ANY, size: wx.Size=wx.Size(1095, 860),
                 pos: wx.Point= wx.DefaultPosition, title='Title',
                 style=MAIN_WINDOW_STYLE, name: str = wx.EmptyString) -> None:
        super().__init__(parent=parent, id=id, size=size, pos=pos, title=title, style=style, name=name)
        self.__toolbar: wx.ToolBar = self.CreateToolBar()
        toolbar_icons = ToolBarIcons(size=24, mask=False)

        btn: wx.ToolBarToolBase = self.__toolbar.CreateTool(toolId=ToolID.FIND_DUPLICATES, label='find',
                                                            bmpNormal=toolbar_icons.GetBitmap(ToolID.FIND_DUPLICATES))
        self.__toolbar.Bind(event=wx.EVT_TOOL, handler=self.__find_duplicates, id=ToolID.FIND_DUPLICATES)
        self.__toolbar.AddTool(btn)

    @property
    def toolbar(self) -> wx.ToolBar:
        return self.__toolbar

    def show(self) -> None:
        self.Show(True)
        self.__toolbar.Realize()

    def __find_duplicates(self, _) -> None:
        FindDuplicateWindow()

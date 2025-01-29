from .findDuplicateWindow import FindDuplicateWindow
from settings.enums import ToolID, WidgetID, IconManipulatorID, CreateItemsID
from settings.consts import MAIN_WINDOW_STYLE, PANEL_SIZE
from settings.iconManipulators import IconManipulators
from widgets.mainPanel import MainPanel
import wx


class MainWindow(wx.Frame):
    def __init__(self, *, parent: wx.Window = None, id: int = wx.ID_ANY, size: wx.Size = wx.Size(1095, 860),
                 pos: wx.Point = wx.DefaultPosition, title: str = 'Title',
                 style=MAIN_WINDOW_STYLE, name: str = wx.EmptyString) -> None:
        super().__init__(parent=parent, id=id, size=size, pos=pos, title=title, style=style, name=name)
        sizer = wx.FlexGridSizer(rows=1, cols=2, hgap=0, vgap=0)

        # настраиваем toolbar
        self.__toolbar: wx.ToolBar = self.CreateToolBar()
        #toolbar_height = self.__toolbar.GetSize().GetHeight()
        toolbar_icons = IconManipulators.get_icon_manipulator(IconManipulatorID.TOOLBAR)
        btn: wx.ToolBarToolBase = self.__toolbar.CreateTool(toolId=ToolID.FIND_DUPLICATES, label='find',
                                                            bmpNormal=toolbar_icons.GetBitmap(ToolID.FIND_DUPLICATES))
        self.__toolbar.AddTool(btn)

        self.__left_panel = MainPanel(parent=self, id=WidgetID.LEFT_MAIN_PANEL, size=PANEL_SIZE,
                                      filepath=r'C:/Users/Prosto_Den/Desktop')
        self.__right_panel = MainPanel(parent=self, id=WidgetID.RIGHT_MAIN_PANEL, size=PANEL_SIZE)

        # настраиваем FileViewer
        file_viewer_icons = IconManipulators.get_icon_manipulator(IconManipulatorID.FILE_VIEWER)
        self.__left_panel.file_viewer.SetImageList(file_viewer_icons, wx.IMAGE_LIST_SMALL)
        self.__right_panel.file_viewer.SetImageList(file_viewer_icons, wx.IMAGE_LIST_SMALL)

        # настраиваем статус бар
        #self.__statusbar: wx.StatusBar = self.CreateStatusBar()
        #status_bar_width, status_bar_height = self.__statusbar.GetSize()
        #self.__statusbar.SetSize(wx.Size(status_bar_width, status_bar_height // 3))
        #self.__statusbar.PushStatusText('F5 Move')

        # добавляем виджеты в sizer
        sizer.Add(self.__left_panel, flag=wx.EXPAND)
        sizer.Add(self.__right_panel, flag=wx.EXPAND)

        # привязываем события
        self.__toolbar.Bind(event=wx.EVT_TOOL, handler=lambda _: self.__find_duplicates(), id=ToolID.FIND_DUPLICATES)

        # привязываем sizer
        self.SetSizer(sizer)
        self.Layout()

    def show(self) -> None:
        self.Center()
        self.Show(True)
        self.__toolbar.Realize()
        #self.__statusbar.Show(True)

    def __find_duplicates(self) -> None:
        FindDuplicateWindow()

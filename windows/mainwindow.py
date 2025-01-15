from .findDuplicateWindow import FindDuplicateWindow
from settings.enums import ToolID, WidgetID, IconManipulatorID
from settings.consts import MAIN_WINDOW_STYLE, CONTROL_PANEL_SIZE, LEFT_PANEL_SIZE, RIGHT_PANEL_SIZE
from settings.iconManipulators import IconManipulators
from widgets.controlPanel import ControlPanel, FileViewer
import wx


class MainWindow(wx.Frame):
    def __init__(self, *, parent: wx.Window = None, id: int = wx.ID_ANY, size: wx.Size = wx.Size(1095, 860),
                 pos: wx.Point = wx.DefaultPosition, title: str = 'Title',
                 style=MAIN_WINDOW_STYLE, name: str = wx.EmptyString) -> None:
        super().__init__(parent=parent, id=id, size=size, pos=pos, title=title, style=style, name=name)
        sizer = wx.FlexGridSizer(rows=2, cols=2, hgap=0, vgap=0)

        # настраиваем toolbar
        self.__toolbar: wx.ToolBar = self.CreateToolBar()
        #toolbar_height = self.__toolbar.GetSize().GetHeight()
        toolbar_icons = IconManipulators.get_icon_manipulator(IconManipulatorID.TOOLBAR)
        btn: wx.ToolBarToolBase = self.__toolbar.CreateTool(toolId=ToolID.FIND_DUPLICATES, label='find',
                                                            bmpNormal=toolbar_icons.GetBitmap(ToolID.FIND_DUPLICATES))
        self.__toolbar.AddTool(btn)

        # настраиваем панели
        self.__left_control_panel = ControlPanel(parent=self, id=WidgetID.LEFT_CONTROL_PANEL, size=CONTROL_PANEL_SIZE)
        self.__right_control_panel = ControlPanel(parent=self, id=WidgetID.RIGHT_CONTROL_PANEL,size=CONTROL_PANEL_SIZE)
        self.__left_panel = wx.Panel(parent=self, size=LEFT_PANEL_SIZE)
        self.__right_panel = wx.Panel(parent=self, size=RIGHT_PANEL_SIZE)

        # настраиваем FileViewer
        file_viewer_icons = IconManipulators.get_icon_manipulator(IconManipulatorID.FILE_VIEWER)
        self.__left_file_viewer = FileViewer(parent=self.__left_panel, id=WidgetID.LEFT_FILE_VIEWER)
        self.__right_file_viewer = FileViewer(parent=self.__right_panel, id=WidgetID.RIGHT_FILE_VIEWER,
                          filepath=r'C:\Users\Prosto_Den\Desktop')
        self.__left_file_viewer.SetImageList(file_viewer_icons, wx.IMAGE_LIST_SMALL)
        self.__right_file_viewer.SetImageList(file_viewer_icons, wx.IMAGE_LIST_SMALL)

        # настраиваем статус бар
        #self.__statusbar: wx.StatusBar = self.CreateStatusBar()
        #status_bar_width, status_bar_height = self.__statusbar.GetSize()
        #self.__statusbar.SetSize(wx.Size(status_bar_width, status_bar_height // 3))
        #self.__statusbar.PushStatusText('F5 Move')

        # добавляем виджеты в sizer
        sizer.Add(self.__left_control_panel)
        sizer.Add(self.__right_control_panel)
        sizer.Add(self.__left_panel)
        sizer.Add(self.__right_panel)

        # привязываем события
        self.__toolbar.Bind(event=wx.EVT_TOOL, handler=lambda _: self.__find_duplicates(), id=ToolID.FIND_DUPLICATES)

        # привязываем sizer
        sizer.Fit(self)
        self.SetSizer(sizer)
        self.Layout()

    def show(self) -> None:
        self.Center()
        self.Show(True)
        self.__toolbar.Realize()
        #self.__statusbar.Show(True)

    def __find_duplicates(self) -> None:
        FindDuplicateWindow()

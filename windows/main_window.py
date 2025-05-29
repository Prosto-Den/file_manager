from windows.duplicate_settings_window import DuplicateSettingsWindow
from settings.enums import ToolID, WidgetID, IconManipulatorID
from settings.consts import PANEL_SIZE, DUPLICATE_WINDOW_SIZE
from windows.duplicate_result_window import DuplicateResult
from settings.icon_manipulators import IconManipulators
from widgets.main_panel import MainPanel
from widgets.file_viewer import FileViewer
from typing import Literal
from settings.settings import settings
import wx


class MainWindow(wx.Frame):
    def __init__(self, *, parent: wx.Window = None, id: int = wx.ID_ANY) -> None:
        super().__init__(parent=parent, id=id)
        sizer = wx.FlexGridSizer(rows=1, cols=2, hgap=0, vgap=0)
        self.SetSize(wx.Size(*settings.settings().main_window_size))
        self.SetTitle(settings.translation().main_title)
        self.SetWindowStyle(settings.settings().MAIN_WINDOW_STYLE)

        # настраиваем toolbar
        self.__toolbar: wx.ToolBar = self.CreateToolBar()
        #toolbar_height = self.__toolbar.GetSize().GetHeight()
        toolbar_icons = IconManipulators.get_icon_manipulator(IconManipulatorID.TOOLBAR)
        find_duplicate_btn: wx.ToolBarToolBase = self.__toolbar.CreateTool(toolId=ToolID.FIND_DUPLICATES, label='find',
                                                            bmpNormal=toolbar_icons.GetBitmap(ToolID.FIND_DUPLICATES))
        settings_btn: wx.ToolBarToolBase = self.__toolbar.CreateTool(toolId=ToolID.SETTINGS_ID, label='settings',
                                                            bmpNormal=toolbar_icons.GetBitmap(ToolID.SETTINGS_ID))

        self.__toolbar.AddTool(find_duplicate_btn)
        self.__toolbar.AddTool(settings_btn)

        # создаём панели с виджетами
        #TODO разобраться с передачей size из настроек (а может вообще лучше передавать размер родителя,
        # а внутри уже считать, как надо)
        self.__left_panel = MainPanel(parent=self, id_=WidgetID.LEFT_MAIN_PANEL, size=PANEL_SIZE)
        self.__right_panel = MainPanel(parent=self, id_=WidgetID.RIGHT_MAIN_PANEL, size=PANEL_SIZE)

        #TODO открытые директории тоже надо сохранять в настройках
        self.__left_panel.set_filepath('C:/Users/Prosto_Den/Desktop')
        self.__right_panel.set_filepath('C:/')

        # настраиваем FileViewer
        #TODO зачем я настраиваю FileViewer тут? Это же можно делать внутри панели
        file_viewer_icons = IconManipulators.get_icon_manipulator(IconManipulatorID.FILE_VIEWER)
        file_viewer: FileViewer = self.__left_panel.file_viewer
        file_viewer.SetImageList(file_viewer_icons, wx.IMAGE_LIST_SMALL)
        file_viewer = self.__right_panel.file_viewer
        file_viewer.SetImageList(file_viewer_icons, wx.IMAGE_LIST_SMALL)

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

    def get_panel_filepath(self, panel_side: Literal['LEFT', 'RIGHT']) -> str:
        if panel_side == 'LEFT':
            return self.__left_panel.get_filepath()
        elif panel_side == 'RIGHT':
            return self.__right_panel.get_filepath()
        raise ValueError('Incorrect panel side')

    def __find_duplicates(self) -> None:
        self.Disable()
        DuplicateSettingsWindow(parent=self, size=DUPLICATE_WINDOW_SIZE)
        #DuplicateResult(self)

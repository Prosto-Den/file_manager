from windows.duplicate_settings_window import DuplicateSettingsWindow
from settings.enums import ToolID, WidgetID, IconManipulatorID
from settings.consts import PANEL_SIZE, DUPLICATE_WINDOW_SIZE, MAIN_WINDOW_STYLE, MAIN_WINDOW_SIZE
from windows.duplicate_result_window import DuplicateResult
from framework.utils.file_system import FileSystem
from app_manager import AppManager
from settings.icon_manipulators import IconManipulators
from widgets.main_panel import MainPanel
from typing import Literal, override
import wx


class MainWindow(wx.Frame):
    def __init__(self) -> None:
        """
        Главное окно приложения
        """
        super().__init__(parent=None, id=wx.ID_ANY)
        sizer = wx.FlexGridSizer(rows=1, cols=2, hgap=0, vgap=0)
        self.SetSize(MAIN_WINDOW_SIZE)
        self.SetTitle(AppManager.Translation.main_title)
        self.SetWindowStyle(MAIN_WINDOW_STYLE)

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
        self.__left_panel = MainPanel(parent=self, id_=WidgetID.LEFT_MAIN_PANEL, size=PANEL_SIZE)
        self.__right_panel = MainPanel(parent=self, id_=WidgetID.RIGHT_MAIN_PANEL, size=PANEL_SIZE)

        # задаём пути
        left_panel_path = AppManager.Settings.left_panel_path
        right_panel_path = AppManager.Settings.right_panel_path
        if not FileSystem.is_exists(left_panel_path):
            left_panel_path = FileSystem.get_root_directory()
        if not FileSystem.is_exists(right_panel_path):
            right_panel_path = FileSystem.get_root_directory()
        self.__left_panel.set_filepath(left_panel_path)
        self.__right_panel.set_filepath(right_panel_path)

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

    @override
    def Show(self, show: bool = True) -> None:
        """
        Переопределённый метод Show(). Сначала центрируем окно и создаём toolbar, затем уже показываем окно
        :param show: True - показать окно, False - спрятать окно
        """
        self.Center()
        self.__toolbar.Realize() if show else self.__toolbar.Hide()
        super().Show(show)

    @override
    def Destroy(self) -> bool:
        """
        Переопределённый метод Destroy(). Сначала сохраняем текущие пути виджетов, затем уничтожаем окно
        """
        AppManager.settings().save_panel_path(self.get_panel_filepath('LEFT'), self.get_panel_filepath('RIGHT'))
        return super().Destroy()

    def get_panel_filepath(self, panel_side: Literal['LEFT', 'RIGHT']) -> str:
        """
        Получить текущий путь панели
        :param panel_side: 'LEFT' - получить путь левой панели, 'RIGHT' - получить путь правой панели
        :return: Путь к текущей директории панели
        """
        if panel_side == 'LEFT':
            return self.__left_panel.get_filepath()
        elif panel_side == 'RIGHT':
            return self.__right_panel.get_filepath()
        raise ValueError('Incorrect panel side')

    def __find_duplicates(self) -> None:
        """
        Открыть окно настройки поиска дубликатов
        """
        self.Disable()
        DuplicateSettingsWindow(parent=self, size=DUPLICATE_WINDOW_SIZE)

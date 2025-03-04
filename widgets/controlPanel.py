from __future__ import annotations
from typing import TYPE_CHECKING
from settings.enums import ControlPanelIconID, WindowID, WidgetID, IconManipulatorID
from settings.consts import WHITE
from settings.iconManipulators  import IconManipulators
from framework.utils import FileManipulator
from framework.events import DiskChangedEvent
from windows.createWindow import CreateWindow
import wx


# для возможной работы аннотации типов
if TYPE_CHECKING:
    from widgets.mainPanel import MainPanel
    from widgets.fileViewer import FileViewer


class ControlPanel(wx.Panel):
    def __init__(self, parent: MainPanel, id: int = wx.ID_ANY,
                 pos: wx.Point = wx.DefaultPosition, size: wx.Size = wx.DefaultSize) -> None:
        super().__init__(parent=parent, id=id, pos=pos, size=size, style=wx.SIMPLE_BORDER)

        # создаём layout панели
        self.__create_layout()

        # реакция на события
        self.__choice.Bind(event=wx.EVT_CHOICE, handler=lambda _: self.__change_disk())
        self.__add_btn.Bind(event=wx.EVT_BUTTON, handler=lambda _: self.__summon_create_window())
        self.__back_btn.Bind(event=wx.EVT_BUTTON, handler=lambda _: self.__back())

    @property
    def disk(self) -> str:
        """
        Получить диск, выбранный из выпадающего меню
        :return: Выбранный диск
        """
        return self.__choice_value

    @property
    def current_filepath(self) -> str:
        """
        Получить путь к текущей директории
        :return: Строка с текущей директорий
        """
        return self.__current_filepath.GetValue()

    def set_filepath(self, filepath: str) -> None:
        """
        Установить значение пути к директории для текстовой панели
        :param filepath: Путь к директории
        """
        self.__current_filepath.SetValue(filepath)

    def enable_back_btn(self, enable: bool = True) -> None:
        """
        Метод для отключения/включения кнопки "Назад"
        :param enable: True - включить кнопку, False - выключить
        """
        self.__back_btn.Enable(enable)

    def __create_layout(self) -> None:
        """
        Создать виджеты на панели
        """
        self.SetBackgroundColour(WHITE)
        sizer = wx.GridBagSizer(hgap=5)

        # настраиваем иконки
        control_panel_icons = IconManipulators.get_icon_manipulator(IconManipulatorID.CONTROL_PANEL)
        bitmap = wx.Bitmap()

        # настраиваем виджеты
        # иконка диска
        bitmap.CopyFromIcon(control_panel_icons.GetIcon(ControlPanelIconID.DISK_ICON))
        disk_icon = wx.StaticBitmap(parent=self, bitmap=bitmap)

        # выпадающий список из имеющихся на Пк дисков
        self.__choice = wx.Choice(parent=self, choices=FileManipulator.get_logical_drives())
        self.__choice.SetSelection(0)
        self.__choice_value: str = self.__choice.GetStringSelection()

        # кнопка создания файла
        bitmap.CopyFromIcon(control_panel_icons.GetIcon(ControlPanelIconID.ADD_ICON))
        self.__add_btn = wx.Button(parent=self, label='Создать')
        self.__add_btn.SetBitmap(bitmap)
        self.__add_btn.Fit()

        # кнопка "Назад"
        bitmap.CopyFromIcon(control_panel_icons.GetIcon(ControlPanelIconID.BACK_ARROW))
        self.__back_btn = wx.BitmapButton(parent=self, bitmap=bitmap)
        self.__back_btn.Disable()

        # кнопка "Вперёд"
        # bitmap.CopyFromIcon(control_panel_icons.GetIcon(ControlPanelIconID.FORWARD_ARROW))
        # self.__forward_btn = wx.BitmapButton(parent=self, bitmap=bitmap)
        # self.__forward_btn.Disable()
        # self.__forward_btn.Fit()

        # строка с текущей файловой директорией
        self.__current_filepath = wx.TextCtrl(parent=self, style=wx.TE_READONLY)
        self.__current_filepath.SetBackgroundColour(WHITE)

        # создаём sizer для кнопок
        btn_sizer = wx.GridBagSizer(5, 5)
        btn_sizer.Add(self.__add_btn, (0, 0), flag=wx.ALIGN_CENTRE)
        btn_sizer.Add(self.__back_btn, (0, 1), flag=wx.ALIGN_CENTRE)

        # размещаем виджеты
        sizer.Add(disk_icon, (0, 0), flag=wx.ALIGN_CENTRE)
        sizer.Add(self.__choice, (0, 1), flag=wx.ALIGN_CENTRE)
        sizer.Add(btn_sizer, (0, 2), flag=wx.ALIGN_CENTRE)
        # sizer.Add(self.__add_btn, (0, 2), flag=wx.ALIGN_CENTRE)
        # sizer.Add(self.__back_btn, (0, 3), flag=wx.ALIGN_CENTRE)
        # sizer.Add(self.__forward_btn, (0, 4), flag=wx.ALIGN_CENTRE)
        sizer.Add(self.__current_filepath, (1, 0), span=wx.GBSpan(1, 4), flag=wx.EXPAND | wx.ALL)

        sizer.AddGrowableRow(1)
        sizer.AddGrowableCol(3)

        # подключаем sizer
        self.SetSizer(sizer)
        self.Layout()

    def __summon_create_window(self) -> None:
        """
        Создать всплывающее окно для создания файлов
        """
        main_window: wx.Window = self.FindWindowById(WindowID.MAIN_WINDOW)
        create_window = CreateWindow(self.GetParent())
        main_window.PopupMenu(create_window)

    def __change_disk(self) -> None:
        """
        Сообщить родителю о смене диска
        :return:
        """
        selected_disk = self.__choice.GetStringSelection()
        event = DiskChangedEvent(disk=selected_disk)
        parent: wx.Window = self.GetParent()
        wx.PostEvent(parent.GetEventHandler(), event)

    def __back(self) -> None:
        """
        Вернуться к предыдущей открытой директории
        """
        parent: MainPanel = self.GetParent()
        file_viewer: FileViewer = parent.get_widget(WidgetID.FILE_VIEWER)
        filepath: str = file_viewer.file_history.GetHistoryFile(0)
        file_viewer.file_history.RemoveFileFromHistory(0)
        file_viewer.file_system.change_path_to(filepath)
        file_viewer.update()
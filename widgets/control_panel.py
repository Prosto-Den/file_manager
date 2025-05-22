from __future__ import annotations
from settings.enums import ControlPanelIconID, WindowID, IconManipulatorID
from settings.icon_manipulators  import IconManipulators
from settings.enums import Colours
from framework.utils.file_system import FileSystem
from framework.utils.file_utils import FileUtils
from framework.events import PathChanged
from framework.observer.observer import Observer
from windows.create_window import CreateWindow
from typing import TYPE_CHECKING, override
from settings.settings import settings
import wx


# для возможной работы аннотации типов
if TYPE_CHECKING:
    from widgets.main_panel import MainPanel


#TODO выставить подсказки для всех кнопок!!!
class ControlPanel(wx.Panel, Observer):
    def __init__(self, parent: MainPanel, id: int = wx.ID_ANY,
                 pos: wx.Point = wx.DefaultPosition, size: wx.Size = wx.DefaultSize) -> None:
        wx.Panel.__init__(self, parent=parent, id=id, pos=pos, size=size, style=wx.SIMPLE_BORDER)

        # создаём layout панели
        self.__create_layout()

        self.__file_history = wx.FileHistory()

        # реакция на события
        self.__choice.Bind(event=wx.EVT_CHOICE, handler=lambda _: self.__change_disk())
        self.__add_btn.Bind(event=wx.EVT_BUTTON, handler=lambda _: self.__summon_create_window())
        self.__back_btn.Bind(event=wx.EVT_BUTTON, handler=lambda _: self.__back())
        self.__insert_btn.Bind(event=wx.EVT_BUTTON, handler=lambda _: self.__insert_from_clipboard())

    @override
    def update(self, filepath: str) -> None:
        self.__back_btn.Enable(self.__file_history.GetCount() > 0)
        self.__insert_btn.Enable(not FileSystem.is_clipboard_empty())
        self.set_filepath(filepath)

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

    def add_file_to_history(self, filepath: str) -> None:
        self.__file_history.AddFileToHistory(filepath)

    def __create_layout(self) -> None:
        """
        Создать виджеты на панели
        """
        self.SetBackgroundColour(Colours.WHITE)
        sizer = wx.GridBagSizer(hgap=5)

        # настраиваем иконки
        control_panel_icons = IconManipulators.get_icon_manipulator(IconManipulatorID.CONTROL_PANEL)
        bitmap = wx.Bitmap()

        # настраиваем виджеты
        # иконка диска
        bitmap.CopyFromIcon(control_panel_icons.GetIcon(ControlPanelIconID.DISK_ICON))
        disk_icon = wx.StaticBitmap(parent=self, bitmap=bitmap)

        # выпадающий список из имеющихся на Пк дисков
        self.__choice = wx.Choice(parent=self, choices=FileSystem.get_logical_drives())
        self.__choice.SetSelection(0)
        #self.__choice_value: str = self.__choice.GetStringSelection()

        # кнопка создания файла
        bitmap.CopyFromIcon(control_panel_icons.GetIcon(ControlPanelIconID.ADD_ICON))
        self.__add_btn = wx.Button(parent=self, label=settings.translation().create_label)
        self.__add_btn.SetBitmap(bitmap)
        self.__add_btn.Fit()

        # кнопка "Назад"
        bitmap.CopyFromIcon(control_panel_icons.GetIcon(ControlPanelIconID.BACK_ARROW))
        self.__back_btn = wx.BitmapButton(parent=self, bitmap=bitmap)
        self.__back_btn.SetToolTip(settings.translation().back_tooltip)
        self.__back_btn.Disable()

        # кнопка "Вперёд"
        # bitmap.CopyFromIcon(control_panel_icons.GetIcon(ControlPanelIconID.FORWARD_ARROW))
        # self.__forward_btn = wx.BitmapButton(parent=self, bitmap=bitmap)
        # self.__forward_btn.Disable()
        # self.__forward_btn.Fit()

        # кнопка "Вставить"
        bitmap.CopyFromIcon(control_panel_icons.GetIcon(ControlPanelIconID.INSERT_ICON))
        self.__insert_btn = wx.BitmapButton(parent=self, bitmap=bitmap)
        self.__insert_btn.SetToolTip(settings.translation().insert_tooltip)

        # строка с текущей файловой директорией
        self.__current_filepath = wx.TextCtrl(parent=self, style=wx.TE_READONLY)
        self.__current_filepath.SetBackgroundColour(Colours.WHITE)

        # создаём sizer для кнопок
        btn_sizer = wx.GridBagSizer(5, 5)
        btn_sizer.Add(self.__add_btn, (0, 0), flag=wx.ALIGN_CENTRE)
        btn_sizer.Add(self.__back_btn, (0, 1), flag=wx.ALIGN_CENTRE)
        btn_sizer.Add(self.__insert_btn, (0, 2), flag=wx.ALIGN_CENTER)

        # размещаем виджеты
        sizer.Add(disk_icon, (0, 0), flag=wx.ALIGN_CENTRE)
        sizer.Add(self.__choice, (0, 1), flag=wx.ALIGN_CENTRE)
        sizer.Add(btn_sizer, (0, 2), flag=wx.ALIGN_CENTRE)
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
        event = PathChanged(location=selected_disk)
        parent: MainPanel = self.GetParent()
        wx.PostEvent(parent.GetEventHandler(), event)

    def __back(self) -> None:
        """
        Вернуться к предыдущей открытой директории
        """
        parent: MainPanel = self.GetParent()
        filepath: str = self.__file_history.GetHistoryFile(0)
        self.__file_history.RemoveFileFromHistory(0)
        event = PathChanged(location=filepath)
        wx.PostEvent(parent.GetEventHandler(), event)

    def __insert_from_clipboard(self):
        for file in FileSystem.get_data_from_clipboard():
            FileUtils.copy_file(file, self.current_filepath)

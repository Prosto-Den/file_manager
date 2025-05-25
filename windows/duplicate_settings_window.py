from __future__ import annotations
from settings.enums import WindowID, Colours, FindDuplicateWindowWidgetsID
from settings.consts import DUPLICATE_WINDOW_STYLE
from typing import TYPE_CHECKING, override
from settings.settings import settings
from framework.utils.widgets_helper import WidgetsHelper
from windows.hash_calculator_window import HashCalculatorWindow
from windows.duplicate_result_window import DuplicateResult
from widgets.text_field import TextField
import wx


if TYPE_CHECKING:
    from windows.main_window import MainWindow


# окно с настройками поиска дубликатов
class DuplicateSettingsWindow(wx.Frame):
    def __init__(self, parent: MainWindow, id_ = WindowID.DUPLICATE_WINDOW, size=wx.DefaultSize,
                 pos: wx.Point= wx.DefaultPosition,
                 style=DUPLICATE_WINDOW_STYLE, name: str = wx.EmptyString) -> None:
        super().__init__(parent=parent, id=id_, size=size, pos=pos, style=style, name=name)
        self.SetTitle(settings.translation().duplicate_file_window_title)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        radiobutton_panel = wx.Panel(self)
        directories_panel = wx.Panel(self, id=FindDuplicateWindowWidgetsID.DIRECTORIES_PANEL)
        buttons_panel = wx.Panel(self)

        # добавляем radiobuttons
        radiobutton_sizer = wx.BoxSizer(wx.VERTICAL)
        two_dir_radiobutton = wx.RadioButton(radiobutton_panel, id=FindDuplicateWindowWidgetsID.TWO_DIR_RADIO_BTN,
                                             label=settings.translation().compare_directories_label)

        one_dir_radiobutton = wx.RadioButton(radiobutton_panel, id=FindDuplicateWindowWidgetsID.ONE_DIR_RADIO_BTN,
                                             label=settings.translation().one_directory_label)
        radiobutton_sizer.Add(two_dir_radiobutton, flag=wx.BOTTOM | wx.LEFT | wx.UP, border=5)
        radiobutton_sizer.Add(one_dir_radiobutton, flag=wx.BOTTOM | wx.LEFT, border=5)

        # sizers для панели с директориями
        self.__two_directories_sizer = wx.GridBagSizer(5, 5)
        self.__one_directory_sizer = wx.GridBagSizer(5, 5)
        self.__current_state = 0

        # two directories sizer
        self.__two_directories_sizer.Add(wx.StaticText(directories_panel,
                                                       label=settings.translation().first_directory_label),
                                         (0, 0), flag=wx.ALIGN_CENTRE_VERTICAL | wx.LEFT, border=5)
        text_field = TextField(directories_panel, FindDuplicateWindowWidgetsID.FIRST_DIR_INPUT)
        text_field.set_text_field_value(parent.get_panel_filepath('LEFT'))
        self.__two_directories_sizer.Add(text_field, (0, 1), flag=wx.EXPAND | wx.RIGHT,
                                         border=5)
        self.__two_directories_sizer.Add(wx.StaticText(directories_panel,
                                                       label=settings.translation().second_directory_label),
                                         (1, 0), flag=wx.ALIGN_CENTER | wx.LEFT, border=5)

        text_field = TextField(directories_panel, FindDuplicateWindowWidgetsID.SECOND_DIR_INPUT)
        text_field.set_text_field_value(parent.get_panel_filepath('RIGHT'))
        self.__two_directories_sizer.Add(text_field, (1, 1), flag=wx.EXPAND | wx.RIGHT,
                                         border=5)
        self.__two_directories_sizer.AddGrowableCol(1)

        # one directory sizer
        self.__one_directory_sizer.Add(wx.StaticText(directories_panel,
                                                     label=settings.translation().directory_label), (0, 0),
                                       flag=wx.ALIGN_CENTER | wx.LEFT, border=5)

        text_field = TextField(directories_panel, FindDuplicateWindowWidgetsID.DIR_INPUT)
        text_field.set_text_field_value(parent.get_panel_filepath('LEFT'))
        self.__one_directory_sizer.Add(text_field, (0, 1), flag=wx.EXPAND | wx.RIGHT,
                                       border=5)
        self.__one_directory_sizer.AddGrowableCol(1)

        WidgetsHelper.hide_sizer(self.__one_directory_sizer)

        # sizer для кнопок
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        ok_btn = wx.Button(buttons_panel, label=settings.translation().ok_label)
        cancel_btn = wx.Button(buttons_panel, label=settings.translation().cancel_label)
        button_sizer.Add(ok_btn, flag=wx.UP, border=5)
        button_sizer.Add(cancel_btn, flag=wx.UP, border=5)

        # задаём sizer для панелей
        radiobutton_panel.SetSizer(radiobutton_sizer)
        directories_panel.SetSizer(self.__two_directories_sizer)
        buttons_panel.SetSizer(button_sizer)

        # размещаем панели на главном sizer
        main_sizer.Add(radiobutton_panel, flag=wx.ALL | wx.EXPAND)
        main_sizer.Add(directories_panel, flag=wx.ALL | wx.EXPAND)
        main_sizer.Add(buttons_panel, flag=wx.ALL | wx.EXPAND)

        # подписка на события
        two_dir_radiobutton.Bind(wx.EVT_RADIOBUTTON, self.__switch_sizer)
        one_dir_radiobutton.Bind(wx.EVT_RADIOBUTTON, self.__switch_sizer)
        ok_btn.Bind(wx.EVT_BUTTON, lambda _: self.__start_searching())
        cancel_btn.Bind(wx.EVT_BUTTON, lambda _: self.Destroy())

        self.SetSizer(main_sizer)
        self.SetBackgroundColour(Colours.WHITE)
        self.Show()

    @override
    def Destroy(self) -> bool:
        self.GetParent().Enable()
        return super().Destroy()

    def __start_searching(self) -> None:
        hash_calculator_window = HashCalculatorWindow(self.GetParent())
        if self.__current_state == FindDuplicateWindowWidgetsID.ONE_DIR_RADIO_BTN:
            text_field: TextField = self.FindWindowById(FindDuplicateWindowWidgetsID.DIR_INPUT, self)
            hash_calculator_window.add_path(text_field.get_value())
        else:
            first_text_field: TextField = self.FindWindowById(FindDuplicateWindowWidgetsID.FIRST_DIR_INPUT, self)
            second_text_field: TextField = self.FindWindowById(FindDuplicateWindowWidgetsID.SECOND_DIR_INPUT, self)
            hash_calculator_window.add_path(first_text_field.get_value())
            hash_calculator_window.add_path(second_text_field.get_value())

        #hash_calculator_window.Show()
        DuplicateResult(self.GetParent())
        self.Destroy()

    def __switch_sizer(self, event: wx.CommandEvent) -> None:
        directories_panel: wx.Panel = self.FindWindowById(FindDuplicateWindowWidgetsID.DIRECTORIES_PANEL)
        directories_panel.Freeze()
        match event.GetId():
            case FindDuplicateWindowWidgetsID.TWO_DIR_RADIO_BTN:
                self.__current_state = FindDuplicateWindowWidgetsID.TWO_DIR_RADIO_BTN
                WidgetsHelper.hide_sizer(self.__one_directory_sizer)
                WidgetsHelper.show_sizer(self.__two_directories_sizer)
                directories_panel.SetSizer(self.__two_directories_sizer, False)
            case FindDuplicateWindowWidgetsID.ONE_DIR_RADIO_BTN:
                self.__current_state = FindDuplicateWindowWidgetsID.ONE_DIR_RADIO_BTN
                WidgetsHelper.hide_sizer(self.__two_directories_sizer)
                WidgetsHelper.show_sizer(self.__one_directory_sizer)
                directories_panel.SetSizer(self.__one_directory_sizer, False)
        directories_panel.Layout()
        directories_panel.Thaw()

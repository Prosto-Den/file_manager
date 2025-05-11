from __future__ import annotations

from wx.lib.masked import seconds

from settings.enums import WindowID, Colours, FindDuplicateWindowWidgetsID
from settings.consts import DUPLICATE_WINDOW_STYLE
from typing import TYPE_CHECKING
from settings.settings import Settings
import wx

if TYPE_CHECKING:
    from windows.main_window import MainWindow

class FindDuplicateWindow(wx.Frame):
    def __init__(self, parent: MainWindow, id_ = WindowID.DUPLICATE_WINDOW, size=wx.DefaultSize,
                 pos: wx.Point= wx.DefaultPosition, title='Поиск дубликатов',
                 style=DUPLICATE_WINDOW_STYLE, name: str = wx.EmptyString) -> None:
        super().__init__(parent=parent, id=id_, size=size, pos=pos, title=title, style=style, name=name)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        radiobutton_panel = wx.Panel(self)
        directories_panel = wx.Panel(self, id=FindDuplicateWindowWidgetsID.DIRECTORIES_PANEL)

        # add radiobuttons
        radiobutton_sizer = wx.BoxSizer(wx.VERTICAL)
        two_dir_radiobutton = wx.RadioButton(radiobutton_panel, id=FindDuplicateWindowWidgetsID.TWO_DIR_RADIO_BTN,
                                             label='Сравнить две директории')
        one_dir_radiobutton = wx.RadioButton(radiobutton_panel, id=FindDuplicateWindowWidgetsID.ONE_DIR_RADIO_BTN,
                                             label='Найти дубликаты в директории')
        radiobutton_sizer.Add(two_dir_radiobutton, flag=wx.BOTTOM, border=5)
        radiobutton_sizer.Add(one_dir_radiobutton, flag=wx.BOTTOM, border=5)

        # sizers for directory panel
        self.__two_directories_sizer = wx.GridBagSizer(5, 5)
        self.__one_directory_sizer = wx.GridBagSizer(5, 5)
        # two directories sizer
        self.__two_directories_sizer.Add(wx.StaticText(directories_panel, label='Первая директория:'),
                                         (0, 0), flag=wx.ALIGN_CENTER)
        self.__two_directories_sizer.Add(wx.TextCtrl(directories_panel), (0, 1), flag=wx.EXPAND | wx.RIGHT,
                                         border=5)
        self.__two_directories_sizer.Add(wx.StaticText(directories_panel, label='Вторая директория:'),
                                         (1, 0), flag=wx.ALIGN_CENTER)
        self.__two_directories_sizer.Add(wx.TextCtrl(directories_panel), (1, 1), flag=wx.EXPAND | wx.RIGHT,
                                         border=5)
        self.__two_directories_sizer.AddGrowableCol(1)

        # one directory sizer
        self.__one_directory_sizer.Add(wx.StaticText(directories_panel, label='Директория:'), (0, 0),
                                       flag=wx.ALIGN_CENTER)
        self.__one_directory_sizer.Add(wx.TextCtrl(directories_panel), (0, 1), flag=wx.EXPAND | wx.RIGHT,
                                       border=5)
        self.__one_directory_sizer.AddGrowableCol(1)

        self.__hide_sizer(self.__one_directory_sizer)

        radiobutton_panel.SetSizer(radiobutton_sizer)
        directories_panel.SetSizer(self.__two_directories_sizer)

        main_sizer.Add(radiobutton_panel, flag=wx.ALL | wx.EXPAND)
        main_sizer.Add(directories_panel, flag=wx.ALL | wx.EXPAND)

        two_dir_radiobutton.Bind(wx.EVT_RADIOBUTTON, self.__switch_sizer)
        one_dir_radiobutton.Bind(wx.EVT_RADIOBUTTON, self.__switch_sizer)

        self.SetSizer(main_sizer)
        self.SetBackgroundColour(Colours.WHITE)
        self.Show()

    def __hide_sizer(self, sizer: wx.Sizer) -> None:
        self.__show_sizer(sizer, False)

    @staticmethod
    def __show_sizer(sizer: wx.Sizer, show: bool = True) -> None:
        item: wx.SizerItem
        for item in sizer.GetChildren():
            item.GetWindow().Show(show)

    def __switch_sizer(self, event: wx.CommandEvent) -> None:
        directories_panel: wx.Panel = self.FindWindowById(FindDuplicateWindowWidgetsID.DIRECTORIES_PANEL)
        directories_panel.Freeze()
        match event.GetId():
            case FindDuplicateWindowWidgetsID.TWO_DIR_RADIO_BTN:
                self.__hide_sizer(self.__one_directory_sizer)
                self.__show_sizer(self.__two_directories_sizer)
                directories_panel.SetSizer(self.__two_directories_sizer, False)
            case FindDuplicateWindowWidgetsID.ONE_DIR_RADIO_BTN:
                self.__hide_sizer(self.__two_directories_sizer)
                self.__show_sizer(self.__one_directory_sizer)
                directories_panel.SetSizer(self.__one_directory_sizer, False)
        directories_panel.Layout()
        directories_panel.Thaw()

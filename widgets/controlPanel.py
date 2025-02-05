import wx
from settings.enums import ControlPanelIconID, WidgetID, IconManipulatorID
from settings.consts import WHITE
from settings.iconManipulators import IconManipulators
from framework.utils import FileManipulator
from framework.events import DiskChangedEvent, BackEvent
from windows.createWindow import CreateWindow


class ControlPanel(wx.Panel):
    def __init__(self, parent: wx.Window, id: int = wx.ID_ANY, filepath: str = None,
                 pos: wx.Point = wx.DefaultPosition, size: wx.Size = wx.DefaultSize) -> None:
        super().__init__(parent=parent, id=id, pos=pos, size=size, style=wx.SIMPLE_BORDER)
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
        self.__back_btn.Fit()
        self.__back_btn.Disable()
        # кнопка "Вперёд"
        bitmap.CopyFromIcon(control_panel_icons.GetIcon(ControlPanelIconID.FORWARD_ARROW))
        self.__forward_btn = wx.BitmapButton(parent=self, bitmap=bitmap)
        self.__forward_btn.Disable()
        self.__forward_btn.Fit()
        # строка с текущей файловой директорией
        self.__current_filepath = wx.TextCtrl(parent=self, style=wx.TE_READONLY)
        self.__current_filepath.SetBackgroundColour(WHITE)

        if filepath is None:
            self.__current_filepath.SetValue(self.__choice_value)
        else:
            self.__current_filepath.SetValue(filepath)

        # размещаем виджеты
        sizer.Add(disk_icon, (0, 0), flag=wx.ALIGN_CENTRE)
        sizer.Add(self.__choice, (0, 1), flag=wx.ALIGN_CENTRE)
        sizer.Add(self.__add_btn, (0, 2), flag=wx.ALIGN_CENTRE)
        sizer.Add(self.__back_btn, (0, 3), flag=wx.ALIGN_CENTRE)
        sizer.Add(self.__forward_btn, (0, 4), flag=wx.ALIGN_CENTRE)
        sizer.Add(self.__current_filepath, (1, 0), span=wx.GBSpan(1, 29), flag=wx.EXPAND)

        # реакция на события
        self.__choice.Bind(event=wx.EVT_CHOICE, handler=lambda _: self.__change_disk())
        self.__add_btn.Bind(event=wx.EVT_BUTTON, handler=lambda _: self.__summon_create_window())
        self.__back_btn.Bind(event=wx.EVT_BUTTON, handler=lambda _: self.__back())

        # подключаем sizer
        self.SetSizer(sizer)
        self.Layout()

    @property
    def disk(self) -> str:
        return self.__choice_value

    @property
    def current_filepath(self) -> str:
        return self.__current_filepath.GetValue()

    def set_filepath(self, filepath: str) -> None:
        self.__current_filepath.SetValue(filepath)

    def unblock_btn(self) -> None:
        self.__back_btn.Enable()

    def block_btn(self) -> None:
        self.__back_btn.Disable()

    def __summon_create_window(self):
        main_window: wx.Window = self.FindWindowById(WidgetID.MAIN_WINDOW)
        create_window = CreateWindow(self.GetParent())
        main_window.PopupMenu(create_window)

    def __change_disk(self) -> None:
        selected_disk = self.__choice.GetStringSelection()
        event = DiskChangedEvent(disk=selected_disk)
        parent: wx.Window = self.GetParent()
        wx.PostEvent(parent.GetEventHandler(), event)

    def __back(self) -> None:
        event = BackEvent()
        parent: wx.Window = self.GetParent()
        wx.PostEvent(parent.GetEventHandler(), event)
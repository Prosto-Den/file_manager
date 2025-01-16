import wx
from settings.enums import ControlPanelIconID, WidgetID, IconManipulatorID
from settings.consts import WHITE
from settings.iconManipulators import IconManipulators
from framework.utils import FileManipulator
from widgets.fileViewer import FileViewer
from windows.createWindow import CreateWindow


class ControlPanel(wx.Panel):
    def __init__(self, parent: wx.Window, id: int = wx.ID_ANY, pos: wx.Point = wx.DefaultPosition,
                 size: wx.Size = wx.DefaultSize) -> None:
        super().__init__(parent=parent, id=id, pos=pos, size=size, style=wx.SIMPLE_BORDER)
        self.SetBackgroundColour(WHITE)
        sizer = wx.GridBagSizer(hgap=5)

        control_panel_icons = IconManipulators.get_icon_manipulator(IconManipulatorID.CONTROL_PANEL)
        bitmap = wx.Bitmap()
        bitmap.CopyFromIcon(control_panel_icons.GetIcon(ControlPanelIconID.DISK_ICON))
        disk_icon = wx.StaticBitmap(parent=self, bitmap=bitmap)

        self.__choice = wx.Choice(parent=self, choices=FileManipulator.get_logical_drives())
        bitmap.CopyFromIcon(control_panel_icons.GetIcon(ControlPanelIconID.ADD_ICON))
        self.__add_btn = wx.Button(parent=self, label='Создать')
        self.__add_btn.SetBitmap(bitmap)
        self.__add_btn.Fit()

        sizer.Add(disk_icon, (0, 0), flag=wx.ALIGN_CENTRE)
        sizer.Add(self.__choice, (0, 1), flag=wx.ALIGN_CENTRE)
        sizer.Add(self.__add_btn, (0, 2), flag=wx.ALIGN_CENTRE)

        self.__choice.SetSelection(0)
        self.__choice_value: str = self.__choice.GetStringSelection()
        self.__choice.Bind(event=wx.EVT_CHOICE, handler=lambda _: self.__change_disk())
        self.__add_btn.Bind(event=wx.EVT_BUTTON, handler=lambda _: self.__test())

        self.SetSizer(sizer)
        self.Layout()

    @property
    def disk(self) -> str:
        return self.__choice_value

    def __test(self):
        main_window: wx.Window = self.FindWindowById(WidgetID.MAIN_WINDOW)
        create_window = CreateWindow()
        main_window.PopupMenu(create_window)

    def __change_disk(self) -> None:
        selected_disk = self.__choice.GetStringSelection()
        file_viewer_id = WidgetID.LEFT_FILE_VIEWER if self.GetId() == WidgetID.LEFT_CONTROL_PANEL \
                                                   else WidgetID.RIGHT_FILE_VIEWER
        file_viewer: FileViewer = self.FindWindowById(file_viewer_id)
        file_viewer.file_system.change_path_to(selected_disk, True)

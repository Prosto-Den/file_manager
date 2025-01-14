import wx
from settings.enums import ControlPanelIconID, WidgetID
from settings.consts import ICON_SIZE, WHITE
from settings.iconManipulators import IconManipulators, IconManipulatorID
from framework.utils import FileManipulator
from widgets.fileViewer import FileViewer



class ControlPanel(wx.Panel):
    def __init__(self, parent: wx.Window, id: int = wx.ID_ANY, pos: wx.Point = wx.DefaultPosition,
                 size: wx.Size = wx.DefaultSize) -> None:
        super().__init__(parent=parent, id=id, pos=pos, size=size, style=wx.SIMPLE_BORDER)
        self.SetBackgroundColour(WHITE)
        control_panel_icons = IconManipulators.get_icon_manipulator(IconManipulatorID.CONTROL_PANEL)

        bitmap = wx.Bitmap()
        bitmap.CopyFromIcon(control_panel_icons.GetIcon(ControlPanelIconID.DISK_ICON))
        self.__disk_icon = wx.StaticBitmap(parent=self, bitmap=bitmap)
        self.__choice = wx.Choice(parent=self, pos=wx.Point(ICON_SIZE, 0),
                                  choices=FileManipulator.get_logical_drives())
        self.__choice.SetSelection(0)

        self.__choice.Bind(event=wx.EVT_CHOICE, handler=lambda _: self.__change_disk())

    @property
    def choice(self) -> wx.Choice:
        return self.__choice

    def __change_disk(self) -> None:
        selected_disk = self.__choice.GetStringSelection()
        file_viewer_id = WidgetID.LEFT_FILE_VIEWER if self.GetId() == WidgetID.LEFT_CONTROL_PANEL \
                                                   else WidgetID.RIGHT_FILE_VIEWER
        file_viewer: FileViewer = self.FindWindowById(file_viewer_id)
        file_viewer.file_system.change_path_to(selected_disk, True)
        file_viewer.update()


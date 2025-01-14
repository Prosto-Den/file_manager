import wx
from settings.enums import ControlPanelIconID
from settings.consts import ICON_SIZE
from settings.iconManipulators import IconManipulators, IconManipulatorID
from framework.utils import FileManipulator



class ControlPanel(wx.Panel):
    def __init__(self, parent: wx.Window, id: int = wx.ID_ANY, pos: wx.Point = wx.DefaultPosition,
                 size: wx.Size = wx.DefaultSize) -> None:
        super().__init__(parent=parent, id=id, pos=pos, size=size)
        control_panel_icons = IconManipulators.get_icon_manipulator(IconManipulatorID.CONTROL_PANEL)

        bitmap = wx.Bitmap()
        bitmap.CopyFromIcon(control_panel_icons.GetIcon(ControlPanelIconID.DISK_ICON))
        self.__disk_icon = wx.StaticBitmap(parent=self, bitmap=bitmap)
        self.__choice = wx.Choice(parent=self, pos=wx.Point(ICON_SIZE, 0),
                                  choices=FileManipulator.get_logical_drives())

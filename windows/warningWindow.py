import wx
from settings.iconManipulators import IconManipulators
from settings.enums import IconManipulatorID


class WarningWindow(wx.Frame):
    def __init__(self, parent: wx.Window, id: int = wx.ID_ANY, title: str = ' ',
                 pos: wx.Point = wx.DefaultPosition, size: wx.Size = wx.DefaultSize,
                 style: int = wx.DEFAULT_FRAME_STYLE, name: str = ' ') -> None:
        super().__init__(parent=parent, id=id, title=title, pos=pos, size=size, style=style, name=name)

        icon_manipulator = IconManipulators.get_icon_manipulator(IconManipulatorID.SYSTEM)
        bitmap = wx.Bitmap()
        bitmap.CopyFromIcon(icon_manipulator.GetIcon(0))

        warn_icon = wx.StaticBitmap(parent=self, bitmap=bitmap)
        warn_icon.Centre(wx.VERTICAL)

        self.Show()
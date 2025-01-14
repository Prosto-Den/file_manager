import wx
import os


class IconManipulator(wx.ImageList):
    def __init__(self, *, icons_path: str, size: int, mask: bool) -> None:
        files = os.listdir(icons_path)
        initial_count = len(files)

        super().__init__(width=size, height=size, mask=mask, initialCount=initial_count)

        for file in files:
            icon = wx.Icon(name=icons_path + '/' + file, type=wx.BITMAP_TYPE_PNG)
            self.Add(icon)

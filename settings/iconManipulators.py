import wx
import os


class FileViewerIcons(wx.ImageList):
    def __init__(self, *, size: int, mask: bool) -> None:
        icons_path = os.path.dirname(__file__) + f"/../icons/{size}x{size}"
        initial_count = len(os.listdir(icons_path))

        super().__init__(width=size, height=size, mask=mask, initialCount=initial_count)

        folder_icon = wx.Icon(name=icons_path + '/folder.png', type=wx.BITMAP_TYPE_PNG)
        file_icon = wx.Icon(name=icons_path + '/file.png', type=wx.BITMAP_TYPE_PNG)

        self.Add(folder_icon)
        self.Add(file_icon)

    def __del__(self):
        self.Destroy()


class ToolBarIcons(wx.ImageList):
    def __init__(self, *, size: int, mask: bool) -> None:
        icons_path = os.path.dirname(__file__) + f"/../icons/toolbar/{size}x{size}/"
        initial_count = len(os.listdir(icons_path))

        super().__init__(width=size, height=size, mask=mask, initialCount=initial_count)

        find_duplicates_icon = wx.Icon(name=icons_path + 'find_duplicates.png', type=wx.BITMAP_TYPE_PNG)
        self.Add(find_duplicates_icon)

    def __del__(self):
        self.Destroy()
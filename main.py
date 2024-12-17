import wx
from fileViewer import FileViewer
from window import Window
from enum import IntEnum


class WidgetsId(IntEnum):
    pass


app = wx.App()
folder_icon = wx.Icon(name='./icons/folder.ico', type=wx.BITMAP_TYPE_ICO)
file_icon = wx.Icon(name='./icons/file.ico', type=wx.BITMAP_TYPE_ICO)
duplicates_icon = wx.Icon(name='./icons/find_duplicates_icon.ico', type=wx.BITMAP_TYPE_ICO)
image_list = wx.ImageList(width=32, height=32, initialCount=3, mask=False)
image_list.Add(icon=folder_icon)
image_list.Add(icon=file_icon)
image_list.Add(icon=duplicates_icon)

frame = Window(parent=None, id=wx.ID_ANY, size=wx.Size(1095, 860), title='Title',
                 style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
frame.Center(wx.BOTH)

left_panel = wx.Panel(parent=frame, size=wx.Size(540, 800), pos=wx.Point(0, 10))
right_panel = wx.Panel(parent=frame, size=wx.Size(540, 800), pos=wx.Point(540, 10))

file_viewer1 = FileViewer(parent=left_panel, size=wx.Size(540, 800), id=123,
                          file_path=r'C:\Users\Prosto_Den\Desktop\Test')
file_viewer2 = FileViewer(parent=right_panel, size=wx.Size(540, 800), id=321,
                          file_path=r'C:\Users\Prosto_Den\Desktop\Test1')
file_viewer1.SetImageList(image_list, wx.IMAGE_LIST_SMALL)
file_viewer2.SetImageList(image_list, wx.IMAGE_LIST_SMALL)

frame.show()

app.MainLoop()

image_list.Destroy()
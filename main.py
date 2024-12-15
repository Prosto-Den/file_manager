import wx
from fileViewer import FileViewer


app = wx.App()
folder_icon = wx.Icon(name='./icons/folder.ico', type=wx.BITMAP_TYPE_ICO)
file_icon = wx.Icon(name='./icons/file.ico', type=wx.BITMAP_TYPE_ICO)
image_list = wx.ImageList(width=32, height=32, initialCount=2, mask=False)
image_list.Add(icon=folder_icon)
image_list.Add(icon=file_icon)

frame = wx.Frame(parent=None, id=wx.ID_ANY, size=wx.Size(1095, 850), title='Title',
                 style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
toolbar = frame.CreateToolBar()
frame.Center(wx.BOTH)

left_panel = wx.Panel(parent=frame, size=wx.Size(540, 800), style=wx.SIMPLE_BORDER)
right_panel = wx.Panel(parent=frame, size=wx.Size(540, 800), pos=wx.Point(540, 0))

file_viewer1 = FileViewer(parent=left_panel, size=wx.Size(540, 800))
file_viewer2 = FileViewer(parent=right_panel, size=wx.Size(540, 800))
file_viewer1.SetImageList(image_list, wx.IMAGE_LIST_SMALL)
file_viewer2.SetImageList(image_list, wx.IMAGE_LIST_SMALL)

frame.Show(True)
file_viewer1.Show(True)
file_viewer2.Show(True)

app.MainLoop()

image_list.Destroy()
import wx
from fileViewer import FileViewer
from mainwindow import MainWindow
from settings.fileViewerIcons import FileViewerIcons


app = wx.App()
fileViewerIcons = FileViewerIcons(size=24, mask=False)
frame = MainWindow(parent=None, id=wx.ID_ANY, size=wx.Size(1095, 860), title='Title',
                   style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)
frame.Center(wx.BOTH)

left_panel = wx.Panel(parent=frame, size=wx.Size(540, 800), pos=wx.Point(0, 10))
right_panel = wx.Panel(parent=frame, size=wx.Size(540, 800), pos=wx.Point(540, 10))

file_viewer1 = FileViewer(parent=left_panel, size=wx.Size(540, 800), id=123,
                          file_path=r'C:/')
file_viewer2 = FileViewer(parent=right_panel, size=wx.Size(540, 800), id=321,
                          file_path=r'C:/')

file_viewer1.SetImageList(fileViewerIcons, wx.IMAGE_LIST_SMALL)
file_viewer2.SetImageList(fileViewerIcons, wx.IMAGE_LIST_SMALL)

frame.show()

app.MainLoop()

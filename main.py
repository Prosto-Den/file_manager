import wx
from fileViewer import FileViewer
from mainwindow import MainWindow
from settings.iconManipulators import FileViewerIcons
from settings.enums import WidgetID


app = wx.App()
fileViewerIcons = FileViewerIcons(size=24, mask=False)
frame = MainWindow(parent=None, id=WidgetID.MAIN_WINDOW, size=wx.Size(1095, 860), title='Prosto File Manager',
                   style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)
frame.Center(wx.BOTH)

toolbar_height = frame.toolbar.GetSize().height // 2 - 9

left_panel = wx.Panel(parent=frame, size=wx.Size(540, 800), pos=wx.Point(0, toolbar_height))
right_panel = wx.Panel(parent=frame, size=wx.Size(540, 800), pos=wx.Point(540, toolbar_height))

file_viewer1 = FileViewer(parent=left_panel, size=wx.Size(540, 800), id=WidgetID.LEFT_FILE_VIEWER,)
                          #filepath=r'C:\Users\Prosto_Den\Desktop')
file_viewer2 = FileViewer(parent=right_panel, size=wx.Size(540, 800), id=WidgetID.RIGHT_FILE_VIEWER,
                          filepath=r'C:\Users\Prosto_Den\Desktop')
file_viewer1.SetImageList(fileViewerIcons, wx.IMAGE_LIST_SMALL)
file_viewer2.SetImageList(fileViewerIcons, wx.IMAGE_LIST_SMALL)

frame.show()

app.MainLoop()

# if __name__ == '__main__':
#     app = App()
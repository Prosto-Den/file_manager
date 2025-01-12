import wx
from widgets.fileViewer import FileViewer
from windows.mainwindow import MainWindow
from settings.iconManipulators import FileViewerIcons
from settings.enums import WidgetID
from settings.consts import ICON_SIZE


app = wx.App()
fileViewerIcons = FileViewerIcons(size=ICON_SIZE, mask=False)
frame = MainWindow(id=WidgetID.MAIN_WINDOW, size=wx.Size(1095, 860), title='Prosto File Manager')
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
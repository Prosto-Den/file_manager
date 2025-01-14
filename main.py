import wx
from widgets.fileViewer import FileViewer
from widgets.controlPanel import ControlPanel
from windows.mainwindow import MainWindow
from settings.enums import WidgetID
from settings.consts import MAIN_WINDOW_SIZE, PANEL_SIZE, ICON_SIZE, ICONS_PATH
from settings.iconManipulators import IconManipulators, IconManipulatorID


app = wx.App()
IconManipulators.init(file_viewer_icons=ICONS_PATH + f'/file_viewer/{ICON_SIZE}x{ICON_SIZE}',
                      control_panel_icons=ICONS_PATH + f'/control_panel/{ICON_SIZE}x{ICON_SIZE}',
                      toolbar_icons=ICONS_PATH + f'/toolbar/{ICON_SIZE}x{ICON_SIZE}',
                      size=ICON_SIZE,
                      mask=False)

file_viewer_icons = IconManipulators.get_icon_manipulator(IconManipulatorID.FILE_VIEWER)

# FileViewerIcons.init(size=ICON_SIZE, mask=False)
# ToolBarIcons.init(size=ICON_SIZE, mask=False)
# ControlPanelIcons.init(size=ICON_SIZE, mask=False)
frame = MainWindow(id=WidgetID.MAIN_WINDOW, size=MAIN_WINDOW_SIZE, title='Prosto File Manager')
frame.Center(wx.BOTH)
toolbar_height = frame.GetToolBar().GetSize().GetHeight() // 2 - 9

#TODO может быть сделать фабрику для ControlPanel?
left_control_panel = ControlPanel(parent=frame, size=wx.Size(540, 24), pos=wx.Point(0, toolbar_height))
right_control_panel = ControlPanel(parent=frame, size=wx.Size(540, 24), pos=wx.Point(540, toolbar_height))
left_panel = wx.Panel(parent=frame, size=PANEL_SIZE, pos=wx.Point(0, toolbar_height + 24))
right_panel = wx.Panel(parent=frame, size=PANEL_SIZE, pos=wx.Point(540, toolbar_height + 24))

file_viewer1 = FileViewer(parent=left_panel, id=WidgetID.LEFT_FILE_VIEWER)
                          #filepath=r'C:\Users\Prosto_Den\Desktop')
file_viewer2 = FileViewer(parent=right_panel, id=WidgetID.RIGHT_FILE_VIEWER,
                          filepath=r'C:\Users\Prosto_Den\Desktop')
file_viewer1.SetImageList(file_viewer_icons, wx.IMAGE_LIST_SMALL)
file_viewer2.SetImageList(file_viewer_icons, wx.IMAGE_LIST_SMALL)

frame.show()
app.MainLoop()

# if __name__ == '__main__':
#     app = App()
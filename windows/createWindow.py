import wx
from settings.iconManipulators import IconManipulators
from settings.enums import IconManipulatorID, FileViewerIconID, CreateItemsID


class CreateWindow(wx.Menu):
    def __init__(self):
        super().__init__()

        icons = IconManipulators.get_icon_manipulator(IconManipulatorID.FILE_VIEWER)
        bitmap = wx.Bitmap()
        bitmap.CopyFromIcon(icons.GetIcon(FileViewerIconID.FOLDER_ICON))

        create_folder = wx.MenuItem(id=CreateItemsID.FOLDER, text='Папку')
        create_folder.SetBitmap(bitmap)

        self.Append(create_folder)

        self.Bind(event=wx.EVT_MENU, handler=self.__test)

    def __test(self, event: wx.CommandEvent):
        print(event.GetId())
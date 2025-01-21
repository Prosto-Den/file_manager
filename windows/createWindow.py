import wx
from settings.iconManipulators import IconManipulators
from settings.enums import IconManipulatorID, FileViewerIconID, CreateItemsID


class CreateWindow(wx.Menu):
    def __init__(self, parent: wx.Window):
        super().__init__()
        self.__parent = parent

        icons = IconManipulators.get_icon_manipulator(IconManipulatorID.FILE_VIEWER)
        bitmap = wx.Bitmap()
        bitmap.CopyFromIcon(icons.GetIcon(FileViewerIconID.FOLDER_ICON))

        create_folder = wx.MenuItem(id=CreateItemsID.FOLDER, text='Папку')
        create_file = wx.MenuItem(id=CreateItemsID.TEXT_FILE, text='Текстовый файл')
        create_folder.SetBitmap(bitmap)

        self.Append(create_folder)
        self.Append(create_file)

        self.Bind(event=wx.EVT_MENU, handler=self.__create)

    def __create(self, event: wx.CommandEvent):
        match event.GetId():
            case CreateItemsID.FOLDER:
                pass
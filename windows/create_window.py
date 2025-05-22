import wx
from settings.icon_manipulators import IconManipulators
from settings.enums import IconManipulatorID, FileViewerIconID, CreateItemsID, FileFormatID
from framework.events import CreateEvent
from settings.settings import settings


class CreateWindow(wx.Menu):
    def __init__(self, parent: wx.Window):
        super().__init__()
        self.__parent = parent

        icons = IconManipulators.get_icon_manipulator(IconManipulatorID.FILE_VIEWER)
        bitmap = wx.Bitmap()

        create_folder = wx.MenuItem(id=CreateItemsID.FOLDER, text=settings.translation().create_directory_label)
        create_file = wx.MenuItem(id=CreateItemsID.TEXT_FILE, text=settings.translation().create_text_file)
        create_docx = wx.MenuItem(id=CreateItemsID.DOCX_FILE, text=settings.translation().create_word_file)

        bitmap.CopyFromIcon(icons.GetIcon(FileViewerIconID.FOLDER_ICON))
        create_folder.SetBitmap(bitmap)
        bitmap.CopyFromIcon(icons.GetIcon(FileViewerIconID.TEXT_FILE_ICON))
        create_file.SetBitmap(bitmap)
        bitmap.CopyFromIcon(icons.GetIcon(FileViewerIconID.WORD_FILE_ICON))
        create_docx.SetBitmap(bitmap)

        self.Append(create_folder)
        self.Append(create_file)
        self.Append(create_docx)

        self.Bind(event=wx.EVT_MENU, handler=self.__create)

    def __create(self, event: wx.CommandEvent):
        event_id = event.GetId()
        match event_id:
            case CreateItemsID.TEXT_FILE:
                file_type = FileFormatID.TXT
            case CreateItemsID.DOCX_FILE:
                file_type = FileFormatID.DOCX
            case _:
                file_type = -1

        create_event = CreateEvent(type=event.GetId(), file_type=file_type)
        wx.PostEvent(self.__parent.GetEventHandler(), create_event)

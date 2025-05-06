import wx
from framework.utils.file_system import FileSystem
from widgets.control_panel import ControlPanel
from widgets.file_viewer import FileViewer
from framework.events import EVT_DISK_CHANGED, DiskChangedEvent, EVT_CREATE, CreateEvent
from settings.consts import CONTROL_PANEL_SIZE, WIDGET
from settings.enums import CreateItemsID, WidgetID


class MainPanel(wx.Panel):
    def __init__(self, parent: wx.Window, id: int = wx.ID_ANY, pos: wx.Point = wx.DefaultPosition,
                 size: wx.Size = wx.DefaultSize, style: int = wx.TAB_TRAVERSAL, name: str = wx.PanelNameStr) -> None:
        super().__init__(parent=parent, id=id, pos=pos, size=size, style=style, name=name)

        self.__create_layout()

        self.Bind(event=EVT_DISK_CHANGED, handler=self.__change_file_viewer_disk)
        self.Bind(event=EVT_CREATE, handler=self.__create)

    def get_widget(self, widget_id: int) -> WIDGET:
        return self.FindWindowById(widget_id, self)

    def set_filepath(self, filepath: str) -> None:
        self.__control_panel.set_filepath(filepath)
        self.__file_viewer.file_system.change_path_to(filepath)

    @property
    def current_filepath(self) -> str:
        return self.__control_panel.current_filepath

    @property
    def file_system(self) -> FileSystem:
        return self.__file_viewer.file_system

    def __create_layout(self) -> None:
        # настройка sizer'а
        sizer = wx.FlexGridSizer(rows=2, cols=1, vgap=0, hgap=0)
        sizer.AddGrowableRow(idx=1)

        # виджеты
        self.__control_panel = ControlPanel(parent=self, size=CONTROL_PANEL_SIZE, id=WidgetID.CONTROL_PANEL)
        self.__file_viewer = FileViewer(parent=self, id=WidgetID.FILE_VIEWER)

        # размещение виджетов
        sizer.Add(self.__control_panel)
        sizer.Add(self.__file_viewer, flag=wx.EXPAND)
        self.SetSizer(sizer)
        self.Layout()

    def __change_file_viewer_disk(self, event: DiskChangedEvent) -> None:
        self.__file_viewer.file_system.change_path_to(event.disk)

    def __create(self, event: CreateEvent) -> None:
        if event.type == CreateItemsID.FOLDER:
            self.__file_viewer.file_system.create_folder()
        else:
            self.__file_viewer.file_system.create_file(event.file_type)
        # match event.type:
        #     case CreateItemsID.FOLDER:
        #         self.__file_viewer.file_system.create_folder(self.__control_panel.current_filepath)
        #     case CreateItemsID.TEXT_FILE:
        #         self.__file_viewer.file_system.create_file(self.__control_panel.current_filepath, FileFormatID.TXT)
        #     case CreateItemsID.DOCS_FILE:
        #         self.__file_viewer.file_system.create_file(self.__control_panel.current_filepath, FileFormatID.DOCS)
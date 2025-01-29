import wx
from widgets.controlPanel import ControlPanel
from widgets.fileViewer import FileViewer
from framework.events import EVT_DISK_CHANGED, DiskChangedEvent, EVT_CREATE, CreateEvent
from settings.consts import CONTROL_PANEL_SIZE
from settings.enums import CreateItemsID


class MainPanel(wx.Panel):
    def __init__(self, parent: wx.Window, id: int = wx.ID_ANY, pos: wx.Point = wx.DefaultPosition,
                 size: wx.Size = wx.DefaultSize, style: int = wx.TAB_TRAVERSAL, name: str = wx.PanelNameStr,
                 filepath: str = None) -> None:
        super().__init__(parent=parent, id=id, pos=pos, size=size, style=style, name=name)
        # настройка sizer'а
        sizer = wx.FlexGridSizer(rows=2, cols=1, vgap=0, hgap=0)
        sizer.AddGrowableRow(idx=1)

        # виджеты
        self.__control_panel = ControlPanel(parent=self, size=CONTROL_PANEL_SIZE, filepath=filepath)
        self.__file_viewer = FileViewer(parent=self, filepath=self.__control_panel.current_filepath,
                                        control_panel=self.__control_panel)

        # размещение виджетов
        sizer.Add(self.__control_panel)
        sizer.Add(self.__file_viewer, flag=wx.EXPAND)
        self.SetSizer(sizer)
        self.Layout()

        self.Bind(event=EVT_DISK_CHANGED, handler=self.__change_file_viewer_disk)
        self.Bind(event=EVT_CREATE, handler=self.__create)

    @property
    def control_panel(self) -> ControlPanel:
        return self.__control_panel

    @property
    def file_viewer(self) -> FileViewer:
        return self.__file_viewer

    def __change_file_viewer_disk(self, event: DiskChangedEvent) -> None:
        self.__file_viewer.file_system.change_path_to(event.disk, True)

    def __create(self, event: CreateEvent) -> None:
        match event.GetId():
            case CreateItemsID.FOLDER:
                self.__file_viewer.file_system.create_folder(self.__control_panel.current_filepath)

import wx
from widgets.control_panel import ControlPanel
from widgets.file_viewer import FileViewer
from framework.events import EVT_CREATE, CreateEvent, EVT_PATH_CHANGED, PathChanged, EVT_ADD_FILE_TO_HISTORY, \
    AddFileToHistoryEvent
from settings.consts import CONTROL_PANEL_SIZE
from settings.enums import CreateItemsID, WidgetID
from typing import override


class MainPanel(wx.Panel):
    def __init__(self, parent: wx.Window, id_: int = wx.ID_ANY, pos: wx.Point = wx.DefaultPosition,
                 size: wx.Size = wx.DefaultSize, style: int = wx.TAB_TRAVERSAL, name: str = wx.PanelNameStr) -> None:
        super().__init__(parent=parent, id=id_, pos=pos, size=size, style=style, name=name)

        self.__create_layout()

        # подписываем ControlPanel на обновления FileViewer
        self.__file_viewer.attach(self.__control_panel)

        self.Bind(event=EVT_PATH_CHANGED, handler=self.__change_file_viewer_path)
        self.Bind(event=EVT_ADD_FILE_TO_HISTORY, handler=self.__add_file_to_history)
        self.Bind(event=EVT_CREATE, handler=self.__create)

    @property
    def file_viewer(self) -> FileViewer:
        return self.__file_viewer

    @property
    def control_panel(self) -> ControlPanel:
        return self.__control_panel

    @override
    def Destroy(self) -> bool:
        self.__file_viewer.detach(self.__control_panel)
        return super().Destroy()


    def set_filepath(self, filepath: str) -> None:
        self.__control_panel.set_filepath(filepath)
        self.__file_viewer.file_system.change_path_to(filepath)

    def get_filepath(self) -> str:
        return self.__control_panel.current_filepath

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

    def __change_file_viewer_path(self, event: PathChanged) -> None:
        self.__file_viewer.file_system.change_path_to(event.location)

    def __add_file_to_history(self, event: AddFileToHistoryEvent) -> None:
        self.__control_panel.add_file_to_history(event.filepath)

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

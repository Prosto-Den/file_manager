import wx
from framework.singleton import Singleton
from settings.enums import PopUpItemsID
from .renamewindow import RenameWindow
from settings.consts import ICON_SIZE


class PopUpMenu(metaclass=Singleton):
    __instance: wx.PopupTransientWindow | None = None
    __filepath: str | None = None
    __menu: wx.ListCtrl | None = None
    __event: wx.ListEvent | None = None

    @classmethod
    def init(cls, parent: wx.Window, filepath: str, event: wx.ListEvent,
                 flags: int = wx.BORDER_NONE) -> None:
        cls.destroy()

        cls.__instance = wx.PopupTransientWindow(parent=parent, flags=flags)
        cls.__filepath = filepath
        cls.__menu = wx.ListCtrl(parent=cls.__instance, style=wx.LC_REPORT | wx.LC_NO_HEADER)
        cls.__event = event.Clone()
        cls.__menu.AppendColumn('', width=100)
        cls.__menu.InsertItem(PopUpItemsID.DELETE_BTN, 'Удалить')
        cls.__menu.InsertItem(PopUpItemsID.RENAME_BTN, 'Переименовать')
        cls.__menu.Bind(event=wx.EVT_LIST_ITEM_SELECTED, handler=cls.__perform)
        cls.__instance.Bind(event=wx.EVT_KILL_FOCUS, handler=lambda _: print('gneg'))

    @classmethod
    def __perform(cls, event: wx.ListEvent) -> None:
        match event.GetIndex():
            case PopUpItemsID.DELETE_BTN:
                cls.__instance.Parent.file_system.delete_file(cls.__filepath)
            case PopUpItemsID.RENAME_BTN:
                list_ctrl: wx.ListCtrl = cls.__instance.GetParent()
                item_position = list_ctrl.GetItemPosition(cls.__event.GetIndex())
                position = list_ctrl.ClientToScreen(item_position)
                position = wx.Point(position[0] + ICON_SIZE, position[1])
                RenameWindow(cls.__instance.GetParent(), position, cls.__filepath)

        cls.destroy()

    @classmethod
    def is_instance_none(cls) -> bool:
        return cls.__instance is None

    @classmethod
    def destroy(cls) -> None:
        if not cls.is_instance_none():
            cls.__instance.Show(False)
            cls.__instance.Destroy()
            cls.__instance = None
            cls.__filepath = None
            cls.__menu = None
            cls.__event = None

    @classmethod
    def set_position(cls, pos) -> None:
        cls.__instance.SetPosition(pos)

    @classmethod
    def set_size(cls, size: wx.Size) -> None:
        cls.__instance.SetSize(size)
        cls.__menu.SetSize(size)

    @classmethod
    def show(cls) -> None:
        cls.__instance.Show(True)
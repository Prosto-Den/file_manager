import wx
from framework.singleton import Singleton
from settings.enums import PopUpItemsID


class PopUpMenu(metaclass=Singleton):
    __instance: wx.PopupTransientWindow | None = None
    __filepath: str | None = None
    __menu: wx.ListCtrl | None = None

    @classmethod
    def init(cls, parent: wx.Window, filepath: str,
                 flags: int = wx.BORDER_NONE) -> None:
        if not cls.is_instance_none():
            cls.destroy()

        cls.__instance = wx.PopupTransientWindow(parent=parent, flags=flags)
        cls.__filepath = filepath
        cls.__menu = wx.ListCtrl(parent=cls.__instance, style=wx.LC_REPORT | wx.LC_NO_HEADER)
        cls.__menu.AppendColumn('', width=100)
        cls.__menu.InsertItem(PopUpItemsID.DELETE_BTN, 'Удалить')
        cls.__menu.Bind(event=wx.EVT_LIST_ITEM_SELECTED, handler=cls.__perform)

    @classmethod
    def __perform(cls, event: wx.ListEvent) -> None:
        match event.GetIndex():
            case PopUpItemsID.DELETE_BTN:
                cls.__instance.Parent.file_system.delete_file(cls.__filepath)

        #cls.__instance.Parent.__update()
        cls.destroy()

    @classmethod
    def is_instance_none(cls) -> bool:
        return cls.__instance is None

    @classmethod
    def destroy(cls) -> None:
        if not cls.is_instance_none():
            cls.__instance.Destroy()
            cls.__instance = None
            cls.__filepath = None
            cls.__menu = None

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
import wx
from framework.singleton import Singleton


class PopUpMenu(metaclass=Singleton):
    __instance: wx.PopupWindow | None = None
    __event: wx.ListEvent | None = None
    __menu: wx.ListCtrl | None = None

    @classmethod
    def init(cls, parent: wx.Window, event: wx.ListEvent,
                 flags: int = wx.BORDER_NONE) -> None:
        if not cls.is_instance_none():
            cls.destroy()

        cls.__instance = wx.PopupWindow(parent=parent, flags=flags)
        cls.__event = event
        print(event.GetText())
        cls.__menu = wx.ListCtrl(parent=cls.__instance, style=wx.LC_REPORT | wx.LC_NO_HEADER)
        cls.__menu.AppendColumn('', width=100)
        cls.__menu.InsertItem(0, 'Удалить')
        cls.__menu.Bind(event=wx.EVT_RIGHT_DOWN, handler=cls.__test)

    @classmethod
    def __test(cls, event: wx.MouseEvent):
        print(cls.__instance)

    @classmethod
    def __test1(cls):
        cls.__instance.Destroy()

    @classmethod
    def is_instance_none(cls):
        return cls.__instance is None

    @classmethod
    def destroy(cls):
        if not cls.is_instance_none():
            cls.__instance.Destroy()
            cls.__instance = None
            cls.__event = None
            cls.__menu = None

    @classmethod
    def set_position(cls, pos) -> None:
        cls.__instance.SetPosition(pos)

    @classmethod
    def set_size(cls, size: wx.Size) -> None:
        cls.__instance.SetSize(size)
        cls.__menu.SetSize(size)

    @classmethod
    def show(cls):
        cls.__instance.Show(True)
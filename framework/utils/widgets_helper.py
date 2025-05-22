import wx


class WidgetsHelper:
    @classmethod
    def show_sizer(cls, sizer: wx.Sizer, show: bool = True) -> None:
        item: wx.SizerItem
        for item in sizer.GetChildren():
            if isinstance(item, wx.Sizer):
                cls.show_sizer(item, show)
            else:
                item.GetWindow().Show(show)

    @classmethod
    def hide_sizer(cls, sizer: wx.Sizer) -> None:
        cls.show_sizer(sizer, False)

import wx


class Panel(wx.Panel):
    """
        Inherited from class wx.Panel
            Parameters:
                parent: wx.Window - the window parent,
                id: int - the panel identifier,
                pos: wx.Point - the panel position,
                size: wx.Size - the panel size,
                style: int - the panel style,
                name: str - the name of the panel
        """
    def __init__(self, parent: wx.Window, id: int = wx.ID_ANY, pos: wx.Point = wx.DefaultPosition,
                 size: wx.Size = wx.DefaultSize, style: int = wx.TAB_TRAVERSAL,
                 name: str = wx.PanelNameStr):
        super().__init__(parent=parent, id=id, pos=pos, size=size, style=style, name=name)
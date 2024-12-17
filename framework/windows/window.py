import wx


class Window(wx.Frame):
    """Inherited from class wx.Frame
        Parameters:
            parent: wx.Window - the window parent,
            id: int - the window identifier,
            title: str - the caption to be displayed on the frame's title bar
            pos: wx.Point - the window position,
            size: wx.Size - the window size,
            style: int - the window style,
            name: str - the name of the window,
    """
    def __init__(self, *, parent: wx.Window = None, id: int = wx.ID_ANY,
                 title: str = wx.EmptyString, pos: wx.Point = wx.DefaultPosition, size: wx.Size = wx.DefaultSize,
                 style: int = wx.DEFAULT_FRAME_STYLE, name: str = wx.FrameNameStr) -> None:
        super().__init__(parent=parent, id=id, title=title, pos=pos, size=size, style=style, name=name)


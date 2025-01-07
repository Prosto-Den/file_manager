import wx


class Window(wx.Frame):
    """
    Inherited from class wx.Frame
        Parameters:
            parent: wx.Window - the window parent,
            id: int - the window identifier,
            title: str - the caption to be displayed on the frame's title bar
            pos: wx.Point - the window position,
            size: wx.Size - the window size,
            style: int - the window style,
            name: str - the name of the window
    """
    def __init__(self, *, parent: wx.Window = None, id: int,
                 title: str, pos: wx.Point, size: wx.Size,
                 style: int, name: str) -> None:
        super().__init__(parent=parent, id=id, title=title, pos=pos, size=size, style=style, name=name)


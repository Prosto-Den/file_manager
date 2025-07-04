from app import App



if __name__ == '__main__':
    # приложение
    app = App()
    app.MainLoop()

    # #TODO потом вынести в класс app
    # clipboard = wx.Clipboard.Get()
    # clipboard.Flush()
    # jpype.shutdownJVM()


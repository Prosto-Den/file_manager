import wx
from windows.mainwindow import MainWindow


# Пока что не работает
class App(wx.App):
    def __init__(self, *, redirect: bool = False, filename: str = None,
                 use_best_visual: bool = False, clear_sig_int: bool = True) -> None:
        super().__init__(redirect=redirect, filename=filename, useBestVisual=use_best_visual, clearSigInt=clear_sig_int)

        self.__main_window = MainWindow(parent=None, title='Prosto File Manager')

        self.__main_window.Show(True)
        self.__mainloop()

    def __mainloop(self):
        self.MainLoop()
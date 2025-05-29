import wx
from windows.main_window import MainWindow
from settings.settings import Settings
from framework.logger.logger import Logger


# Пока что не работает
class App(wx.App):
    def __init__(self, *, redirect: bool = False, filename: str = None,
                 use_best_visual: bool = False, clear_sig_int: bool = True) -> None:
        super().__init__(redirect=redirect, filename=filename, useBestVisual=use_best_visual, clearSigInt=clear_sig_int)

        self.__main_window = MainWindow()
        self.__settings = Settings()
        self.__logger = Logger(self.__settings.settings().logger_format)

        self.__main_window.Show(True)
        self.__mainloop()

    @property
    def settings(self) -> Settings:
        return self.__settings

    def __mainloop(self):
        self.MainLoop()

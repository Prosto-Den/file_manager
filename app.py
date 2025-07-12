from windows.main_window import MainWindow
from app_manager import AppManager
from typing import override
import wx


#TODO продумать перезапуск приложения при смене языка
# возможно можно просто уничтожить MainWindow и создать его по новой
# или просто перерисовать каждый виджет отдельно
class App(wx.App):
    """
    Класс приложения
    """
    def __init__(self, *, redirect: bool = False, filename: str = None,
                 use_best_visual: bool = False, clear_sig_int: bool = True) -> None:
        super().__init__(redirect=redirect, filename=filename, useBestVisual=use_best_visual, clearSigInt=clear_sig_int)
        AppManager.init()
        AppManager.start_JVM()
        AppManager.connect_to_database()

        # главное окно приложения
        #self.__main_window = MainWindow(id=WindowID.MAIN_WINDOW)
        #self.__main_window = AppManager.resources().LoadFrame(None, 'MainWindow')
        #res = xrc.XmlResource('ui/main_window.xml')
        self.__main_window = MainWindow()

    @override
    def MainLoop(self) -> None:
        self.__main_window.Show()
        super().MainLoop()
        # код ниже выполнится после закрытия приложения
        AppManager.shutdown_JVM()
        AppManager.Settings.Instance.save_settings()
        # Сохраняем скопированные данные в буфере
        # TODO может быть стоит сделать флаг в настройках на сохранение буфера
        # wx.Clipboard.Get().Flush()

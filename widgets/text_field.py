import wx
from wx.core import EVT_BUTTON
from windows.choose_path_window import ChoosePathWindow
from settings.consts import MOVE_WINDOW_SIZE
from framework.events import EVT_PATH_CHOSEN, PathChosen


class TextField(wx.Panel):
    def __init__(self, parent: wx.Window) -> None:
        super().__init__(parent)
        sizer = wx.BoxSizer()

        self.__text_field = wx.TextCtrl(self)
        self.__choose_btn = wx.Button(self, label='...')
        self.__choose_btn.SetSize(wx.Size(10, 5))
        self.__choose_btn.SetToolTip('Выбрать директорию')

        sizer.Add(self.__text_field, flag=wx.EXPAND | wx.RIGHT, border=3, proportion=1)
        sizer.Add(self.__choose_btn, flag=wx.EXPAND | wx.SHAPED, border=2)

        self.SetSizer(sizer)
        self.Show()

        self.__choose_btn.Bind(EVT_BUTTON, self.__perform)
        self.Bind(EVT_PATH_CHOSEN, self.__path_chosen)

    def set_text_field_value(self, filepath: str) -> None:
        self.__text_field.SetValue(filepath)

    def __path_chosen(self, event: PathChosen) -> None:
        self.set_text_field_value(event.filepath)

    def __perform(self, event: wx.CommandEvent) -> None:
        choose_path = ChoosePathWindow(parent=self, size=MOVE_WINDOW_SIZE)
        choose_path.set_current_filepath('Текущая директория')
        choose_path.set_current_filepath(self.__text_field.GetValue())
        choose_path.Show()

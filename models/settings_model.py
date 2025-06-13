from pydantic import BaseModel, Field


class SettingsModel(BaseModel):
    """
    Модель с настройками программы
    """
    buffer_size: int = Field(..., alias='bufferSize')
    current_language: str = Field(..., alias='currentLanguage')
    time_format: str = Field(..., alias='timeFormat')
    logger_format: str = Field(..., alias='loggerFormat')
    icon_size: int = Field(..., alias='iconSize')
    main_window_size: list = Field(..., alias='mainWindowSize')
    panel_size: list = Field(..., alias='panelSize')
    control_panel_size: list = Field(..., alias='controlPanelSize')
    file_viewer_size: list = Field(..., alias='fileViewerSize')
    popup_menu_size: list = Field(..., alias='popupMenuSize')
    duplicate_window_size: list = Field(..., alias='popupMenuSize')
    move_window_size: list = Field(..., alias='moveWindowSize')
    MAIN_WINDOW_STYLE: int
    RENAME_WINDOW_STYLE: int
    DUPLICATE_WINDOW_STYLE: int
    FILE_VIEWER_STYLE: int

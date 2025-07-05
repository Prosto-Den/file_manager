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
    left_panel_path: str = Field(..., alias='leftPanelPath')
    right_panel_path: str = Field(..., alias = 'rightPanelPath')

from pydantic import BaseModel, Field


class SettingsModel(BaseModel):
    time_format: str = Field(..., alias='timeFormat')
    icon_size: int = Field(..., alias='iconSize')
    main_window_size: list = Field(..., alias='mainWindowSize')
    panel_size: list = Field(..., alias='panelSize')
    control_panel_size: list = Field(..., alias='controlPanelSize')
    file_viewer_size: list = Field(..., alias='fileViewerSize')
    popup_menu_size: list = Field(..., alias='popupMenuSize')
    duplicate_window_size: list = Field(..., alias='popupMenuSize')
    move_window_size: list = Field(..., alias='moveWindowSize')

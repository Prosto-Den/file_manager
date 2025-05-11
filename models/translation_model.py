from pydantic import BaseModel, Field


class TranslationModel(BaseModel):
    create_label: str = Field(..., alias='create')
    back_label: str = Field(..., alias='back')
    copy_window_title: str = Field(..., alias='copyWindowTitle')
    copy_into: str = Field(..., alias='copyInto')
    copy_label: str = Field(..., alias='copy')
    create_directory_label: str = Field(..., alias='createDirectory')
    create_text_file: str = Field(..., alias='createTextFile')
    create_word_file: str = Field(..., alias='createWordFile')
    find_duplicate_file_window_title: str = Field(..., alias='findDuplicateFileWindowTitle')
    move_window_title: str = Field(..., alias='moveWindowTitle')
    move_into: str = Field(..., alias='moveInto')
    move_label: str = Field(..., alias='move')
    delete_label: str = Field(..., alias='delete')
    rename_label: str = Field(..., alias='rename')
    compare_directories_label: str = Field(..., alias='compareDirectories')
    one_directory_label: str = Field(..., alias='oneDirectoryLabel')
    first_directory_label: str = Field(..., alias='firstDirectory')
    second_directory_label: str = Field(..., alias='secondDirectory')
    directory_label: str = Field(..., alias='directory')
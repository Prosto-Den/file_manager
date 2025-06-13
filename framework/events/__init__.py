import wx.lib.newevent as _ne

PathChanged, EVT_PATH_CHANGED = _ne.NewEvent() # событие изменения просматриваемый директории
PathChosen, EVT_PATH_CHOSEN = _ne.NewEvent() # событие с выбором пути
CreateEvent, EVT_CREATE = _ne.NewEvent() # событие с созданием файла
AddFileToHistoryEvent, EVT_ADD_FILE_TO_HISTORY = _ne.NewEvent() # событие с добавлением пути в историю

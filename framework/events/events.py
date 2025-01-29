import wx.lib.newevent as _ne

PathChangedEvent, EVT_PATH_CHANGED = _ne.NewEvent()
DiskChangedEvent, EVT_DISK_CHANGED = _ne.NewEvent()
CreateEvent, EVT_CREATE = _ne.NewEvent()
RenameEvent, EVT_RENAME = _ne.NewEvent()
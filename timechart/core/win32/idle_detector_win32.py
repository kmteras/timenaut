from timechart.core.settings import Settings
import win32api


def is_idle():
    return (win32api.GetTickCount() - win32api.GetLastInputInfo()) / 1000 > Settings().idle_time

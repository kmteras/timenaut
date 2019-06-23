import psutil
import win32gui
import win32process

from timechart.core.models.process import Process
from timechart.core.models.window import Window


def get_process_data() -> (Process, Window):
    path = None

    window = win32gui.GetForegroundWindow()

    title = win32gui.GetWindowText(window)

    if title == '':
        title = None

    pid = win32process.GetWindowThreadProcessId(window)

    try:
        path = psutil.Process(pid[-1]).exe()
    except psutil.NoSuchProcess as e:
        pass

    return Process(path), Window(title)

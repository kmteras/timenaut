import psutil
import win32gui
import win32process


def get_process_data():
    data = {
        'path': None,
        'title': None
    }

    window = win32gui.GetForegroundWindow()

    title = win32gui.GetWindowText(window)

    if title == '':
        title = None

    data['title'] = title

    pid = win32process.GetWindowThreadProcessId(window)

    try:
        data['path'] = psutil.Process(pid[-1]).exe()
    except psutil.NoSuchProcess as e:
        pass

    return data

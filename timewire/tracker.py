import sys


def get_process_data():
    if sys.platform == 'linux':
        import tracker_linux
        return tracker_linux.get_process_data()
    elif sys.platform == 'win32':
        import tracker_win32
        return tracker_win32.get_process_data()

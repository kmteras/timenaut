import sys


def get_process_data():
    if sys.platform == "linux":
        import tracker_linux
        return tracker_linux.get_process_data()

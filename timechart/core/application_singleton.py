import logging
import os
import sys

if sys.platform != "win32":
    import fcntl


class ApplicationSingletonException(Exception):
    pass


class ApplicationSingleton:
    def __init__(self, lockfile: str):
        self.init = False
        self.lockfile = lockfile

        self.fp = None
        try:
            self.create_lockfile()
        except (IOError, OSError):
            raise ApplicationSingletonException()

        self.init = True

    def __del__(self):
        if not self.init:
            return

        try:
            self.close_lockfile()
        except Exception as e:
            logging.warn(e)
        self.close_server()

    def create_lockfile(self):
        if sys.platform == 'win32':
            self.fp = os.open(self.lockfile, os.O_CREAT | os.O_EXCL | os.O_RDWR)
        else:
            self.fp = open(self.lockfile, 'w')
            self.fp.flush()

            fcntl.lockf(self.fp, fcntl.LOCK_EX | fcntl.LOCK_NB)

    def close_lockfile(self):
        if sys.platform == 'win32':
            if hasattr(self, 'fd'):
                os.close(self.fd)
                os.unlink(self.lockfile)
        else:
            fcntl.lockf(self.fp, fcntl.LOCK_UN)

            if os.path.isfile(self.lockfile):
                os.unlink(self.lockfile)

    def create_server(self):
        pass

    def close_server(self):
        pass

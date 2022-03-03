import sys


class AddSysPath():
    def __init__(self, path):
        self._path = path

    def __enter__(self):
        sys.path.insert(0, str(self._path))

    def __exit__(self, exc_type, exc_value, traceback):
        del sys.path[0]

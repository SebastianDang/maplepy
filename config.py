import sys
import json

if sys.version_info >= (3, 4):
    import pathlib
    path = str(pathlib.Path(__file__).parent.absolute())
else:
    import os
    path = str(os.path.dirname(os.path.abspath(__file__)))


class Config:
    def __init__(self, filename):
        self._filename = filename
        self.load()

    def __setitem__(self, key, item):
        self._args[key] = item

    def __getitem__(self, key):
        return self._args[key]

    def load(self):
        print('Loading', self._filename, '...')
        with open(path + "/" + self._filename) as json_file:
            self._args = json.load(json_file)

    def save(self):
        print('Saving', self._filename, '...')
        with open(path + "/" + self._filename, 'w') as json_file:
            json.dump(self._args, json_file, indent=2)

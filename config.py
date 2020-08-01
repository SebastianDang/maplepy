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
        self.path = path
        self.filename = filename
        self.load()

    def __setitem__(self, key, item):
        self.args[key] = item

    def __getitem__(self, key):
        return self.args[key]

    def load(self):
        print('Loading', self.filename, '...')
        with open(path + "/" + self.filename) as json_file:
            self.args = json.load(json_file)

    def save(self):
        print('Saving', self.filename, '...')
        with open(path + "/" + self.filename, 'w') as json_file:
            json.dump(self.args, json_file, indent=2)

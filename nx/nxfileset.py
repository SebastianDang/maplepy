import os
from nx.nxfile import NXFile


class NXFileSet:

    def __init__(self, *argv):
        self.nxfiles = []
        for arg in argv:
            self.load(arg)

    def load(self, filePath):
        if not os.path.exists(filePath):
            print('{} does not exist'.format(filePath))
            return

        self.nxfiles.append(NXFile(filePath))

    def resolve(self, path):
        for nxfile in self.nxfiles:
            node = nxfile.resolve(path)
            if node:
                return node

        return None

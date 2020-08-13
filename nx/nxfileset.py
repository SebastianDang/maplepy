from nx.nxfile import NXFile


class NXFileSet():

    def __init__(self, *argv):
        self.nxfiles = []
        for arg in argv:
            self.nxfiles.append(NXFile(arg))

    def resolve(self, path):
        for nxfile in self.nxfiles:
            node = nxfile.resolve(path)
            if node:
                return node

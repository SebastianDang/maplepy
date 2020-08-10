class NXSound:

    def __init__(self, nxfile, offset):
        self.nxfile = nxfile
        self.offset = offset

    def getData(self, length):
        self.nxfile.file.seek(self.offset)
        return self.nxfile.file.read(length)
class NXSound:

    def __init__(self, nxfile, offset, length):
        self.nxfile = nxfile
        self.offset = offset
        self.length = length

    def get_data(self):
        """ Get sound data """
        self.nxfile.file.seek(self.offset)
        return self.nxfile.file.read(self.length)

import lz4.block


class NXImage:

    def __init__(self, nxfile, offset, width, height):
        self.nxfile = nxfile
        self.offset = offset
        self.width = width
        self.height = height

    def getData(self):
        self.nxfile.file.seek(self.offset)
        compressedSize = int.from_bytes(self.nxfile.file.read(4), "little")
        compressedBytes = self.nxfile.file.read(compressedSize)
        return lz4.block.decompress(compressedBytes, self.width * self.height * 4, True)

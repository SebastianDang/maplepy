import lz4.block


class NXImage:

    def __init__(self, nxfile, offset):
        self.nxfile = nxfile
        self.offset = offset

    def getData(self, width, height):
        self.nxfile.file.seek(self.offset)
        compressedSize = int.from_bytes(self.nxfile.file.read(4), "little")
        compressedBytes = self.nxfile.file.read(compressedSize)
        return lz4.block.decompress(compressedBytes, width * height * 4, True)

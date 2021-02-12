import lz4.block


class NXImage:

    def __init__(self, nxfile, offset, width, height):
        self.nxfile = nxfile
        self.offset = offset
        self.width = width
        self.height = height

    def get_data(self):
        """ Get image data """
        self.nxfile.file.seek(self.offset)
        compressed_size = int.from_bytes(self.nxfile.file.read(4), 'little')
        compressed_bytes = self.nxfile.file.read(compressed_size)
        return lz4.block.decompress(compressed_bytes, self.width * self.height * 4, True)

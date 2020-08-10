import struct

import nodeparser
from image import Image
from sound import Sound


class NXFile():
    def __init__(self, filePath):
        self.filePath = filePath
        self.file = open(filePath, "rb")
        print(self.file)

        magic = self.file.read(4).decode("ascii")
        if (magic != "PKG4"):
            raise Exception("Cannot read file. Invalid format")
        self.nodeCount = int.from_bytes(self.file.read(4), "little")
        self.nodeOffset = int.from_bytes(self.file.read(8), "little")
        self.stringCount = int.from_bytes(self.file.read(4), "little")
        self.stringOffset = int.from_bytes(self.file.read(8), "little")
        self.imageCount = int.from_bytes(self.file.read(4), "little")
        self.imageOffset = int.from_bytes(self.file.read(8), "little")
        self.soundCount = int.from_bytes(self.file.read(4), "little")
        self.soundOffset = int.from_bytes(self.file.read(8), "little")

        print('nodecount', self.nodeCount)
        print('nodeoffset', self.nodeOffset)
        print('stringCount', self.stringCount)
        print('stringOffset', self.stringOffset)
        print('imageCount', self.imageCount)
        print('imageOffset', self.imageOffset)
        print('soundCount', self.soundCount)
        print('soundOffset', self.soundOffset)

        self.nodes = [None] * self.nodeCount
        self.strings = {}
        self.images = {}
        self.sounds = {}

        # setup tables
        # setup string table
        self.populateStringsTable()

        # setup images

        # self.file.seek(self.imageOffset)
        # for i in range(self.imageCount):
        #     offset = int.from_bytes(self.file.read(8), "little")
        #     self.images[i] = Image(self, offset)

        # # setup sounds

        # self.file.seek(self.soundOffset)
        # for i in range(self.soundCount):
        #     offset = int.from_bytes(self.file.read(8), "little")
        #     self.sounds[i] = Sound(self, offset)

        # populate nodes
        # self.populateNodesTable()

        # self.populateNodeChildren()

        print("done")

    def populateNodesTable(self):
        self.file.seek(self.nodeOffset)
        for i in range(self.nodeCount):
            self.nodes.append(nodeparser.parseNode(self))

    def populateStringsTable(self):
        self.strings = [None] * self.stringCount
        self.file.seek(self.stringOffset)
        for i in range(self.stringCount):
            offset = int.from_bytes(self.file.read(8), "little")
            currentPosition = self.file.tell()
            self.file.seek(offset)
            stringLength = int.from_bytes(self.file.read(2), "little")
            self.strings[i] = self.file.read(stringLength).decode('utf-8')
            self.file.seek(currentPosition)

    def populateNodeChildren(self):
        for node in self.nodes:
            node.populateChildren()

    # lazily get node
    def getNode(self, i):
        node = self.nodes[i]
        if node:
            return node

        self.file.seek(self.nodeOffset + i * 20)  # offset by node size
        self.nodes[i] = nodeparser.parseNode(self)

        return self.nodes[i]

    def getRoot(self):
        return self.getNode(0)

    def resolve(self, path):
        paths = path.split("/")
        node = self.getRoot()
        for path in paths:
            node = node.getChild(path)

        return node

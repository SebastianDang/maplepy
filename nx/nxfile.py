import struct
import logging

import nx.nodeparser as nodeparser


class NXFile():
    """ Read from the NX file format [PKG4] """

    def __init__(self, path, parent=None):

        # Update variables
        self.path = path
        self.parent = parent

        # Open file for reading
        self.file = open(path, 'rb')

        # Check for nx pkg4 type
        magic = self.file.read(4).decode('ascii')
        if magic != 'PKG4':
            raise Exception('Cannot read file. Invalid format')

        # Header info
        self.nodeCount = int.from_bytes(self.file.read(4), 'little')
        self.nodeOffset = int.from_bytes(self.file.read(8), 'little')
        self.stringCount = int.from_bytes(self.file.read(4), 'little')
        self.stringOffset = int.from_bytes(self.file.read(8), 'little')
        self.imageCount = int.from_bytes(self.file.read(4), 'little')
        self.imageOffset = int.from_bytes(self.file.read(8), 'little')
        self.soundCount = int.from_bytes(self.file.read(4), 'little')
        self.soundOffset = int.from_bytes(self.file.read(8), 'little')

        logging.info(f'{self.path}')
        logging.info(f'nodeCount: {self.nodeCount}')
        logging.info(f'nodeOffset: {self.nodeOffset}')
        logging.info(f'stringCount: {self.stringCount}')
        logging.info(f'stringOffset: {self.stringOffset}')
        logging.info(f'imageCount: {self.imageCount}')
        logging.info(f'imageOffset: {self.imageOffset}')
        logging.info(f'soundCount: {self.soundCount}')
        logging.info(f'soundOffset: {self.soundOffset}')

        self.nodes = [None] * self.nodeCount
        self.strings = {}
        self.images = {}
        self.sounds = {}

        # # Setup tables
        # self.populateNodesTable()
        # self.populateStringsTable()
        # self.populateNodeChildren()

        # # Setup images
        # self.file.seek(self.imageOffset)
        # for i in range(self.imageCount):
        #     offset = int.from_bytes(self.file.read(8), 'little')
        #     self.images[i] = Image(self, offset)

        # # Setup sounds
        # self.file.seek(self.soundOffset)
        # for i in range(self.soundCount):
        #     offset = int.from_bytes(self.file.read(8), 'little')
        #     self.sounds[i] = Sound(self, offset)

    def populateNodesTable(self):
        self.file.seek(self.nodeOffset)
        for i in range(self.nodeCount):
            self.nodes[i] = nodeparser.parseNode(self)

    def populateStringsTable(self):
        self.file.seek(self.stringOffset)
        for i in range(self.stringCount):
            offset = int.from_bytes(self.file.read(8), 'little')
            position = self.file.tell()
            self.file.seek(offset)
            length = int.from_bytes(self.file.read(2), 'little')
            self.strings[i] = self.file.read(length).decode('utf-8')
            self.file.seek(position)

    def populateNodeChildren(self):
        for node in self.nodes:
            node.populateChildren()

    def getString(self, index):
        """ Get string by index """

        # If string was already read
        string = self.strings.get(index)
        if string:
            return string

        # Move to string index
        self.file.seek(self.stringOffset + index * 8)

        # Move to location where the string is stored
        self.file.seek(int.from_bytes(self.file.read(8), 'little'))
        length = int.from_bytes(self.file.read(2), 'little')

        # Read and save string
        self.strings[index] = self.file.read(length).decode('utf-8')
        return self.strings[index]

    def getNode(self, index):
        """ Get node by index """

        # If node was already read
        node = self.nodes[index]
        if node:
            return node

        # Move to location the node is stored
        self.file.seek(self.nodeOffset + index * 20)  # offset by node size

        # Read and save node
        self.nodes[index] = nodeparser.parseNode(self)
        return self.nodes[index]

    def getRoot(self):
        """ Return root node """
        return self.getNode(0)

    def resolve(self, path):
        """ Resolve path starting from root """
        return self.getRoot().resolve(path)

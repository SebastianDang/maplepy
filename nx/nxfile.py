import logging
import os
import struct

from nx.nxnode import NXNode


class NXFile():
    """ Read from the NX file format [PKG4] """

    def __init__(self, path, parent=None, populate=None):

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

        # Print header
        self.dumpHeader()

        # Init data
        self.nodes = [None] * self.nodeCount
        self.strings = {}
        self.images = {}
        self.sounds = {}

        # Populate data
        if populate:
            self.populateNodes()
            self.populateNodeChildren()
            self.populateStrings()

    def dumpHeader(self):
        """ Dump header data """

        logging.info(f'{self.path}')
        logging.info(f'nodeCount: {self.nodeCount}')
        logging.info(f'nodeOffset: {self.nodeOffset}')
        logging.info(f'stringCount: {self.stringCount}')
        logging.info(f'stringOffset: {self.stringOffset}')
        logging.info(f'imageCount: {self.imageCount}')
        logging.info(f'imageOffset: {self.imageOffset}')
        logging.info(f'soundCount: {self.soundCount}')
        logging.info(f'soundOffset: {self.soundOffset}')

    def populateNodes(self):
        """ Populate nodes """

        # Begin at the node offset
        self.file.seek(self.nodeOffset)

        # Parse each node
        for i in range(self.nodeCount):
            self.nodes[i] = NXNode.parseNode(self)

    def populateNodeChildren(self):
        """ Populate node's immediate children """

        for node in self.nodes:
            if node:
                node.populateChildren()

    def populateStrings(self):
        """ Populate strings """

        # Begin at the string offset
        self.file.seek(self.stringOffset)

        # Parse each string
        for i in range(self.stringCount):
            offset = int.from_bytes(self.file.read(8), 'little')
            position = self.file.tell()
            self.file.seek(offset)
            length = int.from_bytes(self.file.read(2), 'little')
            self.strings[i] = self.file.read(length).decode('utf-8')
            self.file.seek(position)

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
        self.nodes[index] = NXNode.parseNode(self)
        return self.nodes[index]

    def getRoot(self):
        """ Return root node """
        return self.getNode(0)

    def resolve(self, path):
        """ Resolve path starting from root """
        return self.getRoot().resolve(path)


class NXFileSet:
    """ Create a set of nx files that share data """

    def __init__(self, *argv):

        self.nxfiles = []
        for arg in argv:
            self.load(arg)

    def load(self, path):
        """ Create a new nx file and add it to set """

        # Check if path exists before adding
        if not os.path.exists(path):
            logging.warning(f'{path} does not exist')
            return

        # Create nx file, set parent to self
        self.nxfiles.append(NXFile(path=path, parent=self))

    def resolve(self, path):
        """ Resolve for each file (DFS-like) """

        # Attempt to resolve until success
        for nxfile in self.nxfiles:
            node = nxfile.resolve(path)
            if node:
                return node

        logging.warning(f'{path} failed to resolve')
        return None

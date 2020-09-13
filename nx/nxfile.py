import logging
import os
import struct

from nx.nxnode import NXNode


class NXFile():
    """ Read from the NX file format [PKG4] """

    _MAGIC = 'PKG4'

    def __init__(self, path, parent=None):

        # Update variables
        self.path = path
        self.parent = parent

        # Open file for reading
        self.file = open(path, 'rb')

        # Check for nx pkg4 type
        magic = self.file.read(4).decode('ascii')
        if magic != NXFile._MAGIC:
            raise Exception('Cannot read file. Invalid format')

        # Header info
        self.node_count = int.from_bytes(self.file.read(4), 'little')
        self.node_offset = int.from_bytes(self.file.read(8), 'little')
        self.string_count = int.from_bytes(self.file.read(4), 'little')
        self.string_offset = int.from_bytes(self.file.read(8), 'little')
        self.image_count = int.from_bytes(self.file.read(4), 'little')
        self.image_offset = int.from_bytes(self.file.read(8), 'little')
        self.sound_count = int.from_bytes(self.file.read(4), 'little')
        self.sound_offset = int.from_bytes(self.file.read(8), 'little')

        # Print header
        self.dump_header()

        # Init data
        self.nodes = [None] * self.node_count
        self.strings = {}
        self.images = {}
        self.sounds = {}

    def dump_header(self):
        """ Dump header data """

        logging.info(f'{self.path}')
        logging.info(f'node_count: {self.node_count}')
        logging.info(f'node_offset: {self.node_offset}')
        logging.info(f'string_count: {self.string_count}')
        logging.info(f'string_offset: {self.string_offset}')
        logging.info(f'image_count: {self.image_count}')
        logging.info(f'image_offset: {self.image_offset}')
        logging.info(f'sound_count: {self.sound_count}')
        logging.info(f'sound_offset: {self.sound_offset}')

    def get_node(self, index):
        """ Get node by index """

        # If node was already read
        node = self.nodes[index]
        if node:
            return node

        # Move to location the node is stored
        self.file.seek(self.node_offset + index * 20)  # offset by node size

        # Read and save node
        self.nodes[index] = NXNode.parse_node(self)
        return self.nodes[index]

    def get_root_node(self):
        """ Return root node """
        return self.get_node(0)

    def resolve(self, path):
        """ Resolve path starting from root """
        return self.get_root_node().resolve(path)


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

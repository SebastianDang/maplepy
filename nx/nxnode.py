import struct

from nx.nximage import NXImage
from nx.nxsound import NXSound


class NXNode():

    def __init__(self,  nxfile, nameIndex, childIndex, childCount, type):

        # Constructor
        self.nxfile = nxfile
        self.nameIndex = nameIndex
        self.childIndex = childIndex
        self.childCount = childCount
        self.type = type

        # Variables
        self.childMap = {}
        self.stringIndex = None
        self.imageIndex = None
        self.width = None
        self.height = None
        self.soundIndex = None
        self.length = None
        self._value = None

    def __getitem__(self, key):
        return self.get_child(key)

    @property
    def name(self):
        return self.nxfile.get_string(self.nameIndex)

    @property
    def value(self):
        if self.type == 3:  # string
            return self.nxfile.get_string(self.stringIndex)

        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def populate_children(self):
        """ Populates immediate child nodes. No-ops if ran more than once. """

        # Check if there are any children or already populated
        if self.childCount == 0 or self.childMap:
            return

        # Populate child map
        childMap = {}
        for i in range(self.childIndex, self.childIndex + self.childCount):
            childNode = self.nxfile.get_node(i)
            childMap[childNode.name] = childNode

        # Update variable
        self.childMap = childMap

    def list_children(self):
        """ Lists names of children nodes. """
        self.populate_children()
        return list(self.childMap.keys())

    def get_children(self):
        """ Get children nodes as a list. """
        self.populate_children()
        return list(self.childMap.values())

    def get_child(self, name):
        """ Get child node by name """
        self.populate_children()
        return self.childMap.get(name)

    def get_image(self):
        """ Get image at current index """

        image = self.nxfile.images.get(self.imageIndex)

        if not image:

            # Check for outlink node
            if self['_outlink']:

                # Get path
                value = self['_outlink'].value
                path = value[value.index('/')+1:]

                # Resolve using parent fileset or current file
                if self.nxfile.parent:
                    outlinkNode = self.nxfile.parent.resolve(path)
                else:
                    outlinkNode = self.nxfile.resolve(path)

                # Return outlink node
                if outlinkNode:
                    image = outlinkNode.get_image()
                    self.nxfile.images[self.imageIndex] = image
                    return image

            # Load image from node
            self.nxfile.file.seek(
                self.nxfile.image_offset + self.imageIndex * 8)
            offset = int.from_bytes(self.nxfile.file.read(8), 'little')
            image = NXImage(self.nxfile, offset, self.width, self.height)
            self.nxfile.images[self.imageIndex] = image

        return image

    def get_sound(self):
        """ Get sound at current index """

        sound = self.nxfile.sounds.get(self.soundIndex)

        if not sound:

            # Load sound from node
            self.nxfile.file.seek(
                self.nxfile.sound_offset + self.soundIndex * 8)
            offset = int.from_bytes(self.nxfile.file.read(8), 'little')
            sound = NXSound(self.nxfile, offset)
            self.nxfile.sounds[self.soundIndex] = sound

        return sound.get_data(self.length) if sound else None

    def resolve(self, path):
        """ Get child node by path """

        paths = path.split('/')
        node = self
        for path in paths:
            node = node.get_child(path)
            if not node:
                return None

        return node

    @staticmethod
    def parse_node(nxfile):
        """ Parse the node at the current file pointer """

        file = nxfile.file

        # Unpack format
        # https://docs.python.org/3/library/struct.html#format-characters
        data = struct.unpack('<IIHH', file.read(12))

        # Create node
        node = NXNode(nxfile,
                      nameIndex=data[0],
                      childIndex=data[1],
                      childCount=data[2],
                      type=data[3])

        # Check type
        if node.type == 0:  # null
            file.seek(8, 1)  # skip 8 bytes
        elif node.type == 1:  # long
            node.value = int.from_bytes(file.read(8), 'little', signed=True)
        elif node.type == 2:  # double
            node.value = struct.unpack('<d', file.read(8))
        elif node.type == 3:  # string
            node.stringIndex = int.from_bytes(file.read(4), 'little')
            file.seek(4, 1)
        elif node.type == 4:  # point
            node.x = int.from_bytes(file.read(4), 'little', signed=True)
            node.y = int.from_bytes(file.read(4), 'little', signed=True)
            node.value = (node.x, node.y)  # Use tuple
        elif node.type == 5:  # image
            node.imageIndex = int.from_bytes(file.read(4), 'little')
            node.width = int.from_bytes(file.read(2), 'little')
            node.height = int.from_bytes(file.read(2), 'little')
            node.value = (node.width, node.height)  # Use tuple
        elif node.type == 6:  # sound
            node.soundIndex = int.from_bytes(file.read(4), 'little')
            node.length = int.from_bytes(file.read(4), 'little')
        else:
            raise Exception(
                'Failed to parse node. Encountered invalid node type', node.type)

        return node

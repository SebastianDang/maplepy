import struct

from libnx.nximage import NXImage
from libnx.nxsound import NXSound


class NXNode():

    def __init__(self,  nxfile, name_index, child_index, child_count, type):

        # Constructor
        self.nxfile = nxfile
        self.name_index = name_index
        self.child_index = child_index
        self.child_count = child_count
        self.type = type

        # Children
        self.child_map = {}

        # String
        self.string_index = None

        # Image
        self.image_index = None
        self.width = None
        self.height = None

        # Sound
        self.sound_index = None
        self.length = None

        # Value
        self._value = None

    def __getitem__(self, key):
        return self.get_child(key)

    @property
    def name(self):
        return self.get_string(self.name_index)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def populate_children(self):
        """ Populates immediate child nodes. No-ops if ran more than once. """

        # Check if there are any children or already populated
        if self.child_count == 0 or self.child_map:
            return

        # Populate child map
        child_map = {}
        for i in range(self.child_index, self.child_index + self.child_count):
            child_node = self.nxfile.get_node(i)
            child_map[child_node.name] = child_node

        # Update variable
        self.child_map = child_map

    def list_children(self):
        """ Lists names of children nodes. """
        self.populate_children()
        return list(self.child_map.keys())

    def get_children(self):
        """ Get children nodes as a list. """
        self.populate_children()
        return list(self.child_map.values())

    def get_child(self, name):
        """ Get child node by name """
        self.populate_children()
        return self.child_map.get(name)

    def get_string(self, index):
        """ Get string at current index """

        string = self.nxfile.strings.get(index)

        if not string:

            # Move to string index
            self.nxfile.file.seek(
                self.nxfile.string_offset + index * 8)

            # Move to location where the string is stored
            self.nxfile.file.seek(int.from_bytes(
                self.nxfile.file.read(8), 'little'))
            length = int.from_bytes(self.nxfile.file.read(2), 'little')

            # Read and save string
            self.nxfile.strings[index] = self.nxfile.file.read(
                length).decode('utf-8')
            return self.nxfile.strings[index]

        return string

    def get_image(self):
        """ Get image at current index """

        image = self.nxfile.images.get(self.image_index)

        if not image:

            # Check for outlink node
            if self['_outlink']:

                # Get path
                value = self['_outlink'].value
                path = value[value.index('/')+1:]

                # Resolve using parent fileset or current file
                if self.nxfile.parent:
                    outlink_node = self.nxfile.parent.resolve(path)
                else:
                    outlink_node = self.nxfile.resolve(path)

                # Return outlink node
                if outlink_node:
                    image = outlink_node.get_image()
                    self.nxfile.images[self.image_index] = image
                    return image

            # Load image from node
            self.nxfile.file.seek(
                self.nxfile.image_offset + self.image_index * 8)
            offset = int.from_bytes(self.nxfile.file.read(8), 'little')
            image = NXImage(self.nxfile, offset, self.width, self.height)
            self.nxfile.images[self.image_index] = image

        return image

    def get_sound(self):
        """ Get sound at current index """

        sound = self.nxfile.sounds.get(self.sound_index)

        if not sound:

            # Load sound from node
            self.nxfile.file.seek(
                self.nxfile.sound_offset + self.sound_index * 8)
            offset = int.from_bytes(self.nxfile.file.read(8), 'little')
            sound = NXSound(self.nxfile, offset)
            self.nxfile.sounds[self.sound_index] = sound

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
                      name_index=data[0],
                      child_index=data[1],
                      child_count=data[2],
                      type=data[3])

        # Check type
        if node.type == 0:  # no data
            file.seek(8, 1)  # skip 8 bytes
        elif node.type == 1:  # long
            node.value = int.from_bytes(file.read(8), 'little', signed=True)
        elif node.type == 2:  # double
            node.value = struct.unpack('<d', file.read(8))
        elif node.type == 3:  # string
            node.string_index = int.from_bytes(file.read(4), 'little')
            node.value = node.get_string(node.string_index)
        elif node.type == 4:  # point
            node.x = int.from_bytes(file.read(4), 'little', signed=True)
            node.y = int.from_bytes(file.read(4), 'little', signed=True)
            node.value = (node.x, node.y)
        elif node.type == 5:  # image
            node.image_index = int.from_bytes(file.read(4), 'little')
            node.width = int.from_bytes(file.read(2), 'little')
            node.height = int.from_bytes(file.read(2), 'little')
            # node.value = node.get_image()
        elif node.type == 6:  # sound
            node.sound_index = int.from_bytes(file.read(4), 'little')
            node.length = int.from_bytes(file.read(4), 'little')
            # node.value = node.get_sound()
        else:
            raise Exception(
                'Failed to parse node. Encountered invalid node type', node.type)

        return node

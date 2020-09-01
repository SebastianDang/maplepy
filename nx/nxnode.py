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
        return self.getChild(key)

    @property
    def name(self):
        return self.nxfile.getString(self.nameIndex)

    @property
    def value(self):
        if self.type == 3:  # string
            return self.nxfile.getString(self.stringIndex)

        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def populateChildren(self):
        """ Populates immediate child nodes. No-ops if ran more than once. """

        # Check if there are any children or already populated
        if self.childCount == 0 or self.childMap:
            return

        # Populate child map
        childMap = {}
        for i in range(self.childIndex, self.childIndex + self.childCount):
            childNode = self.nxfile.getNode(i)
            childMap[childNode.name] = childNode

        # Update variable
        self.childMap = childMap

    def listChildren(self):
        """ Lists names of children nodes. """
        self.populateChildren()
        return list(self.childMap.keys())

    def getChildren(self):
        """ Get children nodes as a list. """
        self.populateChildren()
        return list(self.childMap.values())

    def getChild(self, name):
        """ Get child node by name """
        self.populateChildren()
        return self.childMap.get(name)

    def resolve(self, path):
        """ Get child node by path """

        paths = path.split('/')
        node = self
        for path in paths:
            node = node.getChild(path)
            if not node:
                return None

        return node

    def getImage(self):
        """ Get image at current index """

        image = self.nxfile.images.get(self.imageIndex)

        if not image:

            # Check for outlink node
            if self['_outlink']:
                value = self['_outlink'].value
                outlinkNode = self.nxfile.resolve(value[value.index('/')+1:])
                if outlinkNode:
                    image = outlinkNode.getImage()
                    self.nxfile.images[self.imageIndex] = image
                    return image

            # Load image from node
            self.nxfile.file.seek(
                self.nxfile.imageOffset + self.imageIndex * 8)
            offset = int.from_bytes(self.nxfile.file.read(8), 'little')
            image = NXImage(self.nxfile, offset, self.width, self.height)
            self.nxfile.images[self.imageIndex] = image

        return image

    def getSound(self):
        """ Get sound at current index """

        sound = self.nxfile.sounds.get(self.soundIndex)

        if not sound:

            # Load sound from node
            self.nxfile.file.seek(
                self.nxfile.soundOffset + self.soundIndex * 8)
            offset = int.from_bytes(self.nxfile.file.read(8), 'little')
            sound = NXSound(self.nxfile, offset)
            self.nxfile.sounds[self.soundIndex] = sound

        return sound.getData(self.length) if sound else None

from nx.nximage import NXImage
from nx.nxsound import NXSound


class NXNode():

    def __init__(self,  nxfile, nameIndex, childIndex, childCount, type):
        self.nxfile = nxfile
        self.nameIndex = nameIndex
        self.childIndex = childIndex
        self.childCount = childCount
        self.type = type
        self.childMap = {}
        self.didPopulateChildren = False
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
        """Populates immediate child nodes. No-ops if ran more than once.
        """
        if self.didPopulateChildren:
            pass

        if self.childCount == 0:
            pass

        for i in range(self.childIndex, self.childIndex + self.childCount):
            childNode = self.nxfile.getNode(i)
            self.childMap[childNode.name] = childNode

        self.didPopulateChildren = True

    def listChildren(self):
        """Lists names of children nodes.
        """
        self.populateChildren()
        return list(self.childMap.keys())

    def getChildren(self):
        """Get children nodes as a list.
        """
        self.populateChildren()
        return list(self.childMap.values())

    def getChild(self, name):
        self.populateChildren()
        return self.childMap[name]

    def resolve(self, path):
        paths = path.split("/")
        node = self
        for path in paths:
            node = node.getChild(path)

        return node

    def getImage(self):
        image = self.nxfile.images.get(self.imageIndex)

        if not image:
            image = self.loadImage(self.nxfile, self.imageIndex)

        return image.getData(self.width, self.height)

    def loadImage(self, nxfile, imageIndex):
        # currentPos = nxfile.file.tell()
        nxfile.file.seek(nxfile.imageOffset + imageIndex * 8)
        offset = int.from_bytes(nxfile.file.read(8), "little")
        image = NXImage(nxfile, offset)
        nxfile.images[imageIndex] = image
        # nxfile.file.seek(currentPos)
        return image

    def getSound(self):
        sound = self.nxfile.sounds.get(self.soundIndex)

        if not sound:
            sound = self.loadSound(self.nxfile, self.soundIndex)

        return sound.getData(self.length)

    def loadSound(self, nxfile, soundIndex):
        # currentPos = nxfile.file.tell()
        nxfile.file.seek(nxfile.soundOffset + soundIndex * 8)
        offset = int.from_bytes(nxfile.file.read(8), "little")
        sound = NXSound(nxfile, offset)
        nxfile.sounds[soundIndex] = sound
        # nxfile.file.seek(currentPos)
        return sound

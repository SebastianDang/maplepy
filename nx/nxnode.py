from nx.nximage import NXImage
from nx.nxsound import NXSound


class NXNode():

    def __init__(self, name, nxfile, childIndex, childCount, type):
        self.name = name
        self.nxfile = nxfile
        self.childIndex = childIndex
        self.childCount = childCount
        self.type = type
        self.childMap = {}
        self.didPopulateChildren = False

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
        return self.childMap.get(name)

    def resolve(self, path):
        try:
            splitIndex = path.index("/")
            return self.getChild(path[:splitIndex]).resolve(path[splitIndex+1:])
        except:
            return self.getChild(path)

    def getImage(self):
        image = self.nxfile.images.get(self.imageIndex)

        if not image:
            image = self.loadImage(self.nxfile, self.imageIndex)

        return image.getData(self.width, self.height)

    def loadImage(self, nxfile, imageIndex):
        currentPos = nxfile.file.tell()
        nxfile.file.seek(nxfile.imageOffset + imageIndex * 8)
        offset = int.from_bytes(nxfile.file.read(8), "little")
        image = NXImage(nxfile, offset)
        nxfile.images[imageIndex] = image
        nxfile.file.seek(currentPos)
        return image

    def getSound(self):
        sound = self.nxfile.sounds.get(self.soundIndex)

        if not sound:
            sound = self.loadSound(self.nxfile, self.soundIndex)

        return sound.getData(self.length)

    def loadSound(self, nxfile, soundIndex):
        currentPos = nxfile.file.tell()
        nxfile.file.seek(nxfile.soundOffset + soundIndex * 8)
        offset = int.from_bytes(nxfile.file.read(8), "little")
        sound = NXSound(nxfile, offset)
        nxfile.sounds[soundIndex] = sound
        nxfile.file.seek(currentPos)
        return sound

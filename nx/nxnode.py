from image import Image
from sound import Sound


class NXNode():
    def __init__(self, name, nxfile, childIndex, childCount, type):
        self.name = name
        self.nxfile = nxfile
        self.childIndex = childIndex
        self.childCount = childCount
        self.type = type
        self.childMap = {}

    def populateChildren(self):
        if (self.childCount == 0):
            pass

        for i in range(self.childIndex, self.childIndex + self.childCount):
            childNode = self.nxfile.getNode(i)
            self.childMap[childNode.name] = childNode

    def getChild(self, name):
        if self.childCount == 0:
            pass
        elif len(self.childMap) == 0:
            self.populateChildren()

        return self.childMap.get(name)

    def getImage(self):
        image = self.nxfile.images.get(self.imageIndex)

        if not image:
            image = self.loadImage(self.nxfile, self.imageIndex)

        return image.getData(self.width, self.height)

    def loadImage(self, nxfile, imageIndex):
        currentPos = nxfile.file.tell()
        nxfile.file.seek(nxfile.imageOffset + imageIndex * 8)
        offset = int.from_bytes(nxfile.file.read(8), "little")
        image = Image(nxfile, offset)
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
        sound = Sound(nxfile, offset)
        nxfile.sounds[soundIndex] = sound
        nxfile.file.seek(currentPos)
        return sound

import struct

from nxnode import NXNode


def parseNode(nxfile):
    file = nxfile.file

    nameIndex = int.from_bytes(file.read(4), "little")
    name = nxfile.strings[nameIndex]
    childIndex = int.from_bytes(file.read(4), "little")
    childCount = int.from_bytes(file.read(2), "little")
    type = int.from_bytes(file.read(2), "little")
    node = NXNode(name, nxfile, childIndex, childCount, type)

    # print("name", name)
    # print("childIndex", childIndex)
    # print("childCount", childCount)
    # print("type", type)
    if type == 0:  # null
        file.seek(8, 1)  # skip 8 bytes
    elif type == 1:  # long
        node.value = int.from_bytes(file.read(8), "little")
    elif type == 2:  # double
        node.value = struct.unpack('<d', file.read(8))
    elif type == 3:  # string
        node.stringIndex = int.from_bytes(file.read(4), "little")
        node.value = nxfile.strings[node.stringIndex]
        file.seek(4, 1)
    elif type == 4:  # point
        node.x = int.from_bytes(file.read(4), "little")
        node.y = int.from_bytes(file.read(4), "little")
    elif type == 5:  # image
        node.imageIndex = int.from_bytes(file.read(4), "little")
        node.width = int.from_bytes(file.read(2), "little")
        node.height = int.from_bytes(file.read(2), "little")
    elif type == 6:  # sound
        node.soundIndex = int.from_bytes(file.read(4), "little")
        node.length = int.from_bytes(file.read(4), "little")
    else:
        raise Exception(
            "Failed to parse nodes. Encountered invalid node type", type)

    return node

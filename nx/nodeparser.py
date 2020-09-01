import struct

from nx.nxnode import NXNode


def parseNode(nxfile):

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
    type = node.type
    if type == 0:  # null
        file.seek(8, 1)  # skip 8 bytes
    elif type == 1:  # long
        node.value = int.from_bytes(file.read(8), 'little', signed=True)
    elif type == 2:  # double
        node.value = struct.unpack('<d', file.read(8))
    elif type == 3:  # string
        node.stringIndex = int.from_bytes(file.read(4), 'little')
        file.seek(4, 1)
    elif type == 4:  # point
        node.x = int.from_bytes(file.read(4), 'little', signed=True)
        node.y = int.from_bytes(file.read(4), 'little', signed=True)
        node.value = (node.x, node.y)
    elif type == 5:  # image
        node.imageIndex = int.from_bytes(file.read(4), 'little')
        node.width = int.from_bytes(file.read(2), 'little')
        node.height = int.from_bytes(file.read(2), 'little')
    elif type == 6:  # sound
        node.soundIndex = int.from_bytes(file.read(4), 'little')
        node.length = int.from_bytes(file.read(4), 'little')
    else:
        raise Exception(
            'Failed to parse nodes. Encountered invalid node type', type)

    return node

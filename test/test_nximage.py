import os
from nx.nxfile import NXFile

path = 'P:/Downloads/Resources'  # TODO: Change this to use your nx path


def test_nximage():
    node = NXFile(os.path.join(path, 'map.nx')).resolve(
        "Tile/grassySoil.img/bsc/0")
    byte = node.getImage()
    assert node.name == '0'
    assert node.width == 90
    assert node.height == 60
    assert len(byte) == 90 * 60 * 4

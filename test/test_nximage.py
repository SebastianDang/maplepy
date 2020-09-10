import os

from nx.nxfile import NXFile


def test_nximage():
    node = NXFile(os.path.join(os.path.dirname(__file__),  'map.nx')).resolve(
        "Back/grassySoil_new.img/back/0")
    image = node.getImage()
    byte = image.getData()
    assert node.name == '0'
    assert node.width == 22
    assert node.height == 738
    assert len(byte) == 22 * 738 * 4


def test_nximage2():
    node = NXFile(os.path.join(os.path.dirname(__file__),  'map.nx')).resolve(
        "Tile/grassySoil.img/bsc/0")
    image = node.getImage()
    byte = image.getData()
    assert node.name == '0'
    assert node.width == 90
    assert node.height == 60
    assert len(byte) == 90 * 60 * 4


def test_nximage3():
    node = NXFile(os.path.join(os.path.dirname(__file__),  'map.nx')).resolve(
        "Obj/acc1.img/grassySoil/nature/0/0")
    image = node.getImage()
    byte = image.getData()
    assert node.name == '0'
    assert node.width == 131
    assert node.height == 39
    assert len(byte) == 131 * 39 * 4

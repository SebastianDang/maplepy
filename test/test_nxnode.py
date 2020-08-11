import pytest
import os
from nx.nxfile import NXFile

from maplepy.config import Config
config = Config.instance()
config.init('config.json')
path = config['asset_path']


def test_nxnode_resolve():
    node = NXFile(os.path.join(path, 'map.nx')).getRoot().resolve(
        "Tile/grassySoil.img/bsc/0")
    assert node.width == 90

    node2 = NXFile(os.path.join(path, 'map.nx')).getRoot().getChild('Tile').resolve(
        "grassySoil.img/bsc/0")
    assert node2.width == 90

    node3 = NXFile(os.path.join(path, 'map.nx')).getRoot().getChild('Tile').resolve(
        "grassySoil.img/bsc").getChild('0')
    assert node3.width == 90

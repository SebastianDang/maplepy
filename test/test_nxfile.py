import os

import pytest

from maplepy.config import Config
from nx.nxfile import NXFile

config = Config.instance()
config.init('config.json')
path = config['asset_path']


def test_nxfile():
    # nx_files = ['base.nx', 'character.nx', 'effect.nx', 'etc.nx', 'item.nx', 'map.nx', 'mob.nx', 'morph.nx',
    #             'npc.nx', 'quest.nx', 'reactor.nx', 'skill.nx', 'sound.nx', 'string.nx', 'tamingmob.nx', 'ui.nx']
    nx_files = ['map.nx']
    for nx_file in nx_files:
        file = NXFile(os.path.join(path, nx_file))
        assert isinstance(file, NXFile)

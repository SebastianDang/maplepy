import os
import pygame

from maplepy.sound.bgm import SoundBgm

import maplepy.display.display as display
from maplepy.xml.displayitemsxml import BackgroundSpritesXml, LayeredSpritesXml

from maplepy.xml.mapxml import MapXml


class DisplayXml(display.Display):

    def __init__(self, w, h, path):

        # Create display
        super().__init__(w, h)

        # Other properties
        self.path = path

        # Music
        self.bgm = SoundBgm()

        # Objects in the map
        self.map_xml = None

    def load_map(self, map_id):

        # Check input path
        if not os.path.exists(self.path):
            print('{} does not exist'.format(self.path))
            return

        # Check map_id input
        if not map_id or not map_id.isdigit():
            print('{} is not a valid map id'.format(map_id))
            return

        # Build filename
        map_file = '{}/map.wz/map/map{}/{}.img.xml'.format(
            self.path,  map_id[0:1], map_id)

        # Load xml
        self.map_xml = MapXml()
        self.map_xml.open(map_file)
        self.map_xml.parse_root()

        # Unload all old data
        self.background_sprites = None
        self.layered_sprites.clear()
        self.view.topleft = (0, 0)
        self.view_limit = None

        # Setup and load
        self.setup_map()
        self.setup_back_sprites()
        self.setup_map_sprites()

        # Play bgm
        self.bgm.play()

    def setup_map(self):

        # Check if map xml is loaded
        if not self.map_xml:
            return

        # Check if info was parsed
        if not self.map_xml.info:
            return

        # Get view boundaries
        view_keys = ['VRTop', 'VRLeft', 'VRBottom', 'VRRight']
        if all(key in self.map_xml.info for key in view_keys):
            top = int(self.map_xml.info['VRTop'])
            left = int(self.map_xml.info['VRLeft'])
            bottom = int(self.map_xml.info['VRBottom'])
            right = int(self.map_xml.info['VRRight'])
            self.set_view_limit(left, top, right - left, bottom - top)

        # Load bgm
        if 'bgm' in self.map_xml.info:
            file = '{}/sound.wz/{}.mp3'.format(self.path,
                                               self.map_xml.info['bgm'])
            self.bgm.load(file, file=file)
            self.bgm.volume(1.0)

    def setup_back_sprites(self):

        # Check if map xml is loaded
        if not self.map_xml:
            return

        # Check if background  was parsed
        if not self.map_xml.back_items:
            return

        # Create background
        if not self.background:
            self.background = pygame.Surface((800, 600))  # Native resolution

        # Load sets of sprites only once
        background_sprites = BackgroundSpritesXml()
        bS_set = set([x['bS'] for x in self.map_xml.back_items])
        for bS in bS_set:
            background_sprites.load_xml(self.path, bS)
            background_sprites.load_images(self.path, bS)

        # Load objects after
        background_sprites.load_background(
            self.path, bS, self.map_xml.back_items)

        # Set variable
        self.background_sprites = background_sprites

    def setup_map_sprites(self):

        # Check if map xml is loaded
        if not self.map_xml:
            return

        # Load instances
        for map_items in self.map_xml.map_items:

            # Create sprites
            sprites = LayeredSpritesXml()

            # Tiles
            info = map_items['info']
            if 'tS' in info:
                tS = info['tS']
                sprites.load_xml(self.path, 'tile', tS)
                sprites.load_tiles(self.path, 'tile',
                                   tS, map_items['tiles'])

            # Load sets of sprites only once
            oS_set = set([x['oS'] for x in map_items['objects']])
            for oS in oS_set:
                sprites.load_xml(self.path, 'obj', oS)

            # Load objects after
            sprites.load_objects(self.path, 'obj',
                                 oS, map_items['objects'])

            # Add to list
            self.layered_sprites.append(sprites)

        # Load portals
        sprites = LayeredSpritesXml()
        sprites.load_portals(self.path, self.map_xml.portal_items)
        self.layered_sprites.append(sprites)

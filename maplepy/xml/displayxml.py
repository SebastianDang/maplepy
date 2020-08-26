import os
import pygame

import maplepy.display.display as display
from maplepy.xml.displayitemsxml import BackgroundSpritesXml, LayeredSpritesXml

from maplepy.xml.mapxml import MapXml
from maplepy.sound.bgm import SoundBgm


class DisplayXml(display.Display):

    def __init__(self, w, h, path):

        # Create display
        super().__init__(w, h)

        # Other properties
        self.path = path

        # Music
        self.bgm = None

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
        map_file = "{}/map.wz/map/map{}/{}.img.xml".format(
            self.path,  map_id[0:1], map_id)

        # Load xml
        self.map_xml = MapXml()
        self.map_xml.open(map_file)
        self.map_xml.parse_root()

        # Unload all old data
        self.background_sprites = None
        self.layered_sprites.clear()
        self.view_limit = None

        # Setup and load
        self.setup_map()
        self.setup_back_sprites()
        self.setup_map_sprites()

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

        # Start bgm
        if 'bgm' in self.map_xml.info:
            self.bgm = SoundBgm()
            self.bgm.volume = 1.0
            self.bgm.play_bgm("{}/sound.wz".format(self.path),
                              self.map_xml.info['bgm'])

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

        # If variable is not yet initialized
        if not self.background_sprites:
            self.background_sprites = BackgroundSpritesXml()

        # Get back name (should be unique)
        bS_set = []
        for back in self.map_xml.back_items:
            bS_set.append(back['bS'])
        bS_set = set(bS_set)

        # Load sets of sprites only once
        for bS in bS_set:
            self.background_sprites.load_xml(self.path, bS)
            self.background_sprites.load_images(self.path, bS)

        # Load objects after
        self.background_sprites.load_backgrounds(
            self.path, bS, self.map_xml.back_items)

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

            # Objects
            oS_set = []
            for obj in map_items['objects']:
                oS_set.append(obj['oS'])
            oS_set = set(oS_set)
            for oS in oS_set:
                sprites.load_xml(self.path, 'obj', oS)
            sprites.load_objects(self.path, 'obj',
                                 oS, map_items['objects'])

            # Add to list
            self.layered_sprites.append(sprites)

        # Load portals
        sprites = LayeredSpritesXml()
        sprites.load_portals(self.path, self.map_xml.portal_items)
        self.layered_sprites.append(sprites)

import os
import sys
import pygame
from maplepy.xml.mapxml import MapXml
from maplepy.map.mapsprites import MapSprites
from maplepy.map.backsprites import BackSprites
from maplepy.sound.bgm import SoundBgm


class MapDisplay():

    def __init__(self, w, h, path):

        # Required properties
        self.width = w
        self.height = h
        self.path = path

        # Background surface
        self.background = None

        # User view
        self.view = None
        self.view_limit = None

        # Music
        self.bgm = None

        # Objects in the map
        self.map_xml = None
        self.back_sprites = None
        self.map_sprite_layers = []

        # Status
        self.loaded = False

    def load_map(self, map_id):

        # Status
        self.loaded = False

        # Clear
        self.map_xml = None
        self.back_sprites = None
        self.map_sprite_layers.clear()

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

        # Setup and load
        self.setup_map()
        self.setup_back_sprites()
        self.setup_map_sprites()

        # Status
        self.loaded = True

    def setup_map(self):

        # Check if map xml is loaded
        if not self.map_xml:
            return

        # Check if info was parsed
        if not self.map_xml.info:
            return

        # Set up view
        self.view = pygame.Rect(0, 0, self.width, self.height)

        # Get view boundaries
        view_keys = ['VRTop', 'VRLeft', 'VRBottom', 'VRRight']
        if all(key in self.map_xml.info for key in view_keys):
            top = int(self.map_xml.info['VRTop'])
            left = int(self.map_xml.info['VRLeft'])
            bottom = int(self.map_xml.info['VRBottom'])
            right = int(self.map_xml.info['VRRight'])
            self.view_limit = pygame.Rect(
                left, top, right - left, bottom - top)

        # Start bgm
        if 'bgm' in self.map_xml.info:
            self.bgm = SoundBgm()
            self.bgm.volume = 0.1
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
        if not self.back_sprites:
            self.back_sprites = BackSprites()

        # Get back name (should be unique)
        bS_set = []
        for back in self.map_xml.back_items:
            bS_set.append(back['bS'])
        bS_set = set(bS_set)

        # Load sets of sprites only once
        for bS in bS_set:
            self.back_sprites.load_xml(bS, self.path)
            self.back_sprites.load_sprites(bS, self.path)

        # Load objects after
        self.back_sprites.load_backgrounds(bS, self.map_xml.back_items)

    def setup_map_sprites(self):

        # Check if map xml is loaded
        if not self.map_xml:
            return

        # Load instances
        for map_items in self.map_xml.map_items:

            # Create sprites
            sprites = MapSprites()

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
            self.map_sprite_layers.append(sprites)

    def move_view(self, x, y):
        self.view = self.view.move(x, y)

    def update(self):

        # Camera
        if self.view and self.view_limit:
            self.view = self.view.clamp(self.view_limit)

        # Background
        if self.back_sprites:
            self.back_sprites.update()

        # Tiles / Objs
        for sprites in self.map_sprite_layers:
            sprites.update()

    def blit(self, surface):

        # Background
        if self.back_sprites:

            # Blit onto background surface
            self.background.fill((0, 0, 0))
            self.back_sprites.blit(self.background, self.view)

            # Scale background surface and blit to target surface
            background = pygame.transform.scale(
                self.background, surface.get_size())
            surface.blit(background, surface.get_rect())

        # Tiles / Objs
        for sprites in self.map_sprite_layers:
            sprites.blit(surface, self.view)

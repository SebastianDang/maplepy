import os
import sys
import pygame
from wz.xml.MapXml import MapXml
from wz.map.MapSprites import MapSprites
from wz.map.BackSprites import BackSprites
from wz.sound.Bgm import Sound_Bgm


class MapDisplay():
    def __init__(self, screen):

        # Main screen to draw onto
        self.screen = screen

        # Background to draw onto
        self.background = None

        # Camera movement
        self.cam = None
        self.bounds = None

        # Music
        self.bgm = None

        # Objects in the map
        self.path = '.'
        self.map_xml = None
        self.back_sprites = None
        self.map_sprites = []

    def load_map(self, map_id):

        # Check map_id input
        if not map_id or not map_id.isdigit():
            print('{} is not a valid map id'.format(map_id))
            return

        # Build filename
        file = "{}/map.wz/Map/Map{}/{}.img.xml".format(
            self.path,  map_id[0:1], map_id)

        # Load xml
        self.map_xml = MapXml()
        self.map_xml.open(file)
        self.map_xml.parse_root()

        # Setup map
        self.setup()

        # Load sprites
        self.load_back_sprites()
        self.load_map_sprites()

    def setup(self):

        # Get screen boundaries
        top = int(self.map_xml.info['VRTop'])
        left = int(self.map_xml.info['VRLeft'])
        bottom = int(self.map_xml.info['VRBottom'])
        right = int(self.map_xml.info['VRRight'])
        self.bounds = pygame.Rect(left, top, right - left, bottom - top)

        # Set up camera
        w, h = self.screen.get_size()
        self.cam = pygame.Rect(0, 0, w, h)

        # Get bgm
        if 'bgm' in self.map_xml.info:
            self.bgm = Sound_Bgm()
            self.bgm.play_bgm("{}/Sound.wz".format(self.path),
                              self.map_xml.info['bgm'])

    def load_back_sprites(self):

        # Check if map xml is loaded
        if not self.map_xml:
            return

        # Create background
        if not self.background:
            self.background = pygame.Surface((800, 600))

        # If variable is not yet initialized
        if not self.back_sprites:
            self.back_sprites = BackSprites()

        # Get back name (should be unique)
        bS_set = []
        for back in self.map_xml.all_backs:
            bS_set.append(back['bS'])
        bS_set = set(bS_set)

        # Load sets of sprites only once
        for bS in bS_set:
            self.back_sprites.load_xml(bS, self.path)
            self.back_sprites.load_sprites(bS, self.path)

        # Load objects after
        self.back_sprites.load_objects(bS, self.map_xml.all_backs)

    def load_map_sprites(self):

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
                tile_name = info['tS']
                sprites.load_xml(self.path, 'Tile', tile_name)
                sprites.load_tiles(self.path, 'Tile',
                                   tile_name, map_items['tiles'])

            # Objects
            oS_set = []
            for obj in map_items['objects']:
                oS_set.append(obj['oS'])
            oS_set = set(oS_set)
            for oS in oS_set:
                sprites.load_xml(self.path, 'Obj', oS)
            sprites.load_objects(self.path, 'Obj',
                                 oS, map_items['objects'])

            # Add to lost
            self.map_sprites.append(sprites)

    def update(self):

        # Camera
        if self.cam and self.bounds:
            self.cam = self.cam.clamp(self.bounds)

        # Background
        if self.back_sprites:
            self.back_sprites.update()

        # Tiles / Objs
        for sprites in self.map_sprites:
            sprites.update()

    def blit(self):

        # Background
        if self.back_sprites:
            self.background.fill((0, 0, 0))
            self.back_sprites.blit(self.background, self.cam)
            background = pygame.transform.scale(
                self.background, self.screen.get_size())
            self.screen.blit(background, self.screen.get_rect())

        # Tiles / Objs
        for sprites in self.map_sprites:
            sprites.blit(self.screen, self.cam)

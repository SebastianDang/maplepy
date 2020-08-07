import os
import sys
import pygame
from Wz.Map.Map_xml import Map_xml
from Wz.Back.Back_sprites import Back_sprites
from Wz.Tile.Tile_sprites import Tile_sprites
from Wz.Object.Object_sprites import Object_sprites
from Wz.Sound.Bgm import Sound_Bgm
vec = pygame.math.Vector2


class Map_sprites(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()

        # Main screen to draw onto
        self.screen = screen

        # Background to draw into
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
        self.tile_sprites_list = []
        self.object_sprites = None

    def load_map(self, map_id):

        # Check map_id input
        if not map_id or not map_id.isdigit():
            print('{} is not a valid map id'.format(map_id))
            return

        # Build filename
        file = "{}/Map.wz/Map/Map{}/{}.img.xml".format(
            self.path,  map_id[0:1], map_id)

        # Load xml
        self.map_xml = Map_xml()
        self.map_xml.open(file)
        self.map_xml.parse_root()

    def load_info(self):

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
        if not self.map_xml:
            return

        # Create background
        if not self.background:
            self.background = pygame.Surface((800, 600))

        # If variable is not yet initialized
        if not self.back_sprites:
            self.back_sprites = Back_sprites()

        # Clear objects before beginning
        self.back_sprites.clear_objects()

        # Get back name (should be unique)
        bS_set = []
        for back in self.map_xml.all_backs:
            bS_set.append(back['bS'])
        bS_set = set(bS_set)

        # Load sets of sprites only once
        for bS in bS_set:
            self.back_sprites.load_xml(bS, "{}/Map.wz".format(self.path))
            self.back_sprites.load_sprites(bS, "{}/Map.wz".format(self.path))

        # Load objects after
        self.back_sprites.load_objects(bS, self.map_xml.all_backs)

    def load_tile_sprites(self):
        if not self.map_xml:
            return

        # Load instances
        for object_instances in self.map_xml.all_tiles:
            info = object_instances['info']
            if 'tS' in info:
                # Get tile name
                tile_name = info['tS']
                # Create sprites
                sprites = Tile_sprites()
                sprites.load_xml(tile_name, "{}/Map.wz".format(self.path))
                sprites.load_sprites("{}/Map.wz".format(self.path))
                sprites.load_objects(object_instances['tiles'])
            self.tile_sprites_list.append(sprites)

    def load_object_sprites(self):
        if not self.map_xml:
            return

        # If variable is not yet initialized
        if not self.object_sprites:
            self.object_sprites = Object_sprites()

        # Clear objects before beginning
        self.object_sprites.clear_objects()

        # Load instances
        for object_instances in self.map_xml.all_objects:

            # Load sets of sprites only once
            oS_set = []
            for obj in object_instances['objects']:
                oS_set.append(obj['oS'])
            oS_set = set(oS_set)
            for oS in oS_set:
                self.object_sprites.load_xml(oS, "{}/Map.wz".format(self.path))

            # Load objects after
            self.object_sprites.load_objects(
                object_instances['objects'], "{}/Map.wz".format(self.path))

    def draw_backs(self, offset=None):
        if self.back_sprites:
            self.back_sprites.blit(offset)

    def update_tiles(self):
        for tile_sprites in self.tile_sprites_list:
            tile_sprites.update()

    def draw_tiles(self, offset=None):
        for tile_sprites in self.tile_sprites_list:
            tile_sprites.blit(offset)

    def draw_objects(self, offset=None):
        if self.object_sprites:
            self.object_sprites.blit(offset)

    def update(self):

        # Camera
        if self.cam and self.bounds:
            self.cam = self.cam.clamp(self.bounds)

        # Background
        if self.back_sprites:
            self.back_sprites.update()

        # Tiles
        for tile_sprites in self.tile_sprites_list:
            tile_sprites.update()

        # Objects
        if self.object_sprites:
            self.object_sprites.update()

    def blit(self):

        # Background
        if self.back_sprites:
            self.back_sprites.blit(self.background, self.cam)
            background = pygame.transform.scale(
                self.background, self.screen.get_size())
            self.screen.blit(background, self.screen.get_rect())

        # Tiles
        for tile_sprites in self.tile_sprites_list:
            tile_sprites.blit(self.screen, self.cam)

        # Objects
        if self.object_sprites:
            self.object_sprites.blit(self.screen, self.cam)

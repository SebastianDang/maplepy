import os
import sys
import pygame
from Map.Map_xml import Map_xml
from Back.Back_sprites import Back_sprites
from Tile.Tile_sprites import Tile_sprites
from Object.Object_sprites import Object_sprites
vec = pygame.math.Vector2


class Map_sprites(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        # Camera movement
        self.cam = None
        self.bounds = None
        # Objects in the map
        self.path = '.'
        self.map_xml = None
        self.back_sprites = None
        self.tile_sprites_list = []
        self.object_sprites = None

    def load_map(self, map_id):
        if not map_id or not map_id.isdigit():
            print('{} is not a valid map id'.format(map_id))
            return

        # Build filename
        file = "{}/Map/Map{}/{}.img.xml".format(
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

    def load_back_sprites(self):
        if not self.map_xml:
            return

        # If variable is not yet initialized
        if not self.back_sprites:
            self.back_sprites = Back_sprites(self.screen)

        # Clear objects before beginning
        self.back_sprites.clear_objects()

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
                sprites = Tile_sprites(self.screen)
                sprites.load_xml(tile_name, self.path)
                sprites.load_sprites(self.path)
                sprites.load_objects(object_instances['tiles'])
            self.tile_sprites_list.append(sprites)

    def load_object_sprites(self):
        if not self.map_xml:
            return

        # If variable is not yet initialized
        if not self.object_sprites:
            self.object_sprites = Object_sprites(self.screen)

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
                self.object_sprites.load_xml(oS, self.path)

            # Load objects after
            self.object_sprites.load_objects(
                object_instances['objects'], self.path)

    def update_backs(self):
        if self.back_sprites:
            self.back_sprites.update()

    def draw_backs(self, offset=None):
        if self.back_sprites:
            self.back_sprites.blit(offset)

    def update_tiles(self):
        for tile_sprites in self.tile_sprites_list:
            tile_sprites.update()

    def draw_tiles(self, offset=None):
        for tile_sprites in self.tile_sprites_list:
            tile_sprites.blit(offset)

    def update_objects(self):
        if self.object_sprites:
            self.object_sprites.update()

    def draw_objects(self, offset=None):
        if self.object_sprites:
            self.object_sprites.blit(offset)

    def update(self):
        self.update_backs()
        self.update_objects()

    def blit(self):

        # Update camera
        if self.cam and self.bounds:
            self.cam = self.cam.clamp(self.bounds)

        # Blit
        self.draw_backs(self.cam)
        self.draw_tiles(self.cam)
        self.draw_objects(self.cam)

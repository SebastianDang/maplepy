import os
import pygame

import maplepy.display.display as display
from maplepy.nx.displayitemsnx import BackgroundSpritesNx, LayeredSpritesNx

from maplepy.nx.mapnx import MapNx
from maplepy.sound.bgm import SoundBgm


class DisplayNx(display.Display):

    def __init__(self, w, h, path):

        # Create display
        super().__init__(w, h)

        # Other properties
        self.path = path

        # Objects in the map
        self.map_nx = MapNx()
        self.map_nx.open('{}/map.nx'.format(self.path))

        # Status
        self.loaded = False

    def load_map(self, map_id):

        # Status
        self.loaded = False

        # Unload all old data
        self.background_sprites = None
        self.layered_sprites.clear()
        self.view_limit = None

        # Check map_id input
        if not map_id or not map_id.isdigit():
            print('{} is not a valid map id'.format(map_id))
            return

        # Setup and load
        self.setup_map(map_id)
        self.setup_background_sprites(map_id)
        self.setup_layered_sprites(map_id)

        # Status
        self.loaded = True

    def setup_map(self, map_id):

        # Check if map nx is loaded
        if not self.map_nx.file:
            return

        # Get info
        info = self.map_nx.get_info_data(map_id)
        if not info:
            return

        # Get view boundaries
        view_keys = ['VRTop', 'VRLeft', 'VRBottom', 'VRRight']
        if all(key in info for key in view_keys):
            top = int(info['VRTop'])
            left = int(info['VRLeft'])
            bottom = int(info['VRBottom'])
            right = int(info['VRRight'])
            self.set_view_limit(left, top, right - left, bottom - top)

    def setup_background_sprites(self, map_id):

        # Check if map nx is loaded
        if not self.map_nx.file:
            return

        # Create background
        if not self.background:
            self.background = pygame.Surface((800, 600))  # Native resolution

        # If variable is not yet initialized
        if not self.background_sprites:
            self.background_sprites = BackgroundSpritesNx()

        # Load background
        self.background_sprites.load_background(self.map_nx, map_id)

    def setup_layered_sprites(self, map_id):

        # Check if map nx is loaded
        if not self.map_nx.file:
            return

        # Load layers
        for i in range(0, 8):
            layered_sprites = LayeredSpritesNx()
            layered_sprites.load_layer(self.map_nx, map_id, i)
            self.layered_sprites.append(layered_sprites)

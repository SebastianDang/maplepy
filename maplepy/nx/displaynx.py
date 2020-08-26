import os
import pygame

import maplepy.display.display as display
from maplepy.nx.displayitemsnx import BackgroundSpritesNx, LayeredSpritesNx

from maplepy.nx.mapnx import MapNx
from maplepy.nx.soundnx import SoundNx

map_file_names = ['map.nx', 'map001.nx', 'map002.nx', 'map2.nx']
sound_file_names = ['sound.nx', 'sound001.nx', 'sound2.nx']


class DisplayNx(display.Display):

    def __init__(self, w, h, path):

        # Create display
        super().__init__(w, h)

        # Other properties
        self.path = path
        self.bgm_path = None
        self.bgm = None

        # Objects in the map
        self.map_nx = MapNx()
        for map_file in map_file_names:
            self.map_nx.open('{}/{}'.format(self.path, map_file))

        self.sound_nx = SoundNx()
        for sound_file in sound_file_names:
            self.sound_nx.open('{}/{}'.format(self.path, sound_file))

    def load_map(self, map_id):

        # Check map_id input
        if not map_id or not map_id.isdigit():
            print('{} is not a valid map id'.format(map_id))
            return

        # Check if map nx is loaded
        if not self.map_nx.file:
            return

        # Check if map exists
        if not self.map_nx.get_map_node(map_id):
            return

        # Unload all old data
        self.background_sprites = None
        self.layered_sprites.clear()
        self.view.topleft = (0, 0)
        self.view_limit = None

        # Setup and load
        self.setup_map(map_id)
        self.setup_background_sprites(map_id)
        self.setup_layered_sprites(map_id)

    def setup_map(self, map_id):

        # Check if map nx is loaded
        if not self.map_nx.file:
            return

        # Get info
        info = self.map_nx.get_info_data(map_id)
        minimap = self.map_nx.get_minimap_data(map_id)
        if not info or not minimap:
            return

        # Get view boundaries
        view_keys = ['VRTop', 'VRLeft', 'VRBottom', 'VRRight']
        minimap_keys = ['centerX', 'centerY', 'width', 'height']
        if all(key in info for key in view_keys):
            top = int(info['VRTop'])
            left = int(info['VRLeft'])
            bottom = int(info['VRBottom'])
            right = int(info['VRRight'])
            self.view.topleft = (left, top)
            self.set_view_limit(left, top, right - left, bottom - top)
        elif minimap and all(key in minimap for key in minimap_keys):
            x = int(minimap['centerX'])
            y = int(minimap['centerY'])
            width = int(minimap['width'])
            height = int(minimap['height'])
            self.view.topleft = (-x, -y)
            self.set_view_limit(-x, -y, width, height)

        # Bgm
        if 'bgm' in info and info['bgm'] != self.bgm_path:

            try:

                # Stop previous bgm
                if self.bgm:
                    self.bgm.stop()

                # Play bgm
                self.bgm_path = info['bgm']
                self.bgm = self.sound_nx.get_sound(self.bgm_path)
                if self.bgm:
                    # fade_ms is added because there is a popping sound
                    # in the beginning. fade helps to reduce the pop
                    # TODO: find better solution to the pop sound
                    self.bgm.play(loops=-1, maxtime=0, fade_ms=1000)

            except:
                pass

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

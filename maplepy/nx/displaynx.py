import os
import logging
import random
import time
import pygame

from maplepy.sound.bgm import SoundBgm

import maplepy.display.display as display
from maplepy.nx.displayitemsnx import BackgroundSpritesNx, LayeredSpritesNx

from maplepy.nx.mapnx import MapNx
from maplepy.nx.soundnx import SoundNx

map_file_names = ['map.nx', 'map001.nx', 'map002.nx', 'map2.nx']
sound_file_names = ['sound.nx', 'sound001.nx', 'sound2.nx']
random.seed(time.time())


class DisplayNx(display.Display):

    def __init__(self, w, h, path):

        # Create display
        super().__init__(w, h)

        # Other properties
        self.path = path
        self.bgm = SoundBgm()
        self.maps = None

        # Objects in the map
        self.map_nx = MapNx()
        for file in map_file_names:
            self.map_nx.open(f'{path}/{file}')

        self.sound_nx = SoundNx()
        for file in sound_file_names:
            self.sound_nx.open(f'{path}/{file}')

    def load_random_map(self):

        # Check if map nx is loaded
        if not self.map_nx.file:
            return

        # Load map nodes
        if not self.maps:
            self.maps = self.map_nx.get_map_nodes()

        # Pick random node
        if self.maps:
            choices = list(self.maps.keys())
            map_id = random.choice(choices)[:9]
            logging.info(f'Load random map: {map_id}')
            self.load_map(map_id)

    def load_map(self, map_id):

        # Check map_id input
        if not map_id or not map_id.isdigit():
            logging.warning(f'{map_id} is not a valid map id')
            return

        # Check if map nx is loaded
        if not self.map_nx.file:
            return

        # Check if map exists
        if not self.map_nx.get_map_node(map_id):
            return

        # Unload all old data
        self.view.topleft = (0, 0)
        self.view_limit = None
        self.background_sprites = None
        self.layered_sprites.clear()
        self.overlayed_sprites = None

        # Setup and load
        self.setup_info(map_id)
        self.setup_background_sprites(map_id)
        self.setup_layered_sprites(map_id)
        self.setup_portal_sprites(map_id)

        # Play bgm
        self.bgm.play()

    def setup_info(self, map_id):

        # Check if map nx is loaded
        if not self.map_nx.file:
            return

        # Get info, minimap, foothold
        info = self.map_nx.get_info_data(map_id)
        minimap = self.map_nx.get_minimap_data(map_id)
        foothold = self.map_nx.get_foothold_data(map_id)
        ladder = self.map_nx.get_ladder_data(map_id)

        # Check for required data
        if not info or not minimap:
            return

        # Set view boundaries using VR
        view_keys = ['VRTop', 'VRLeft', 'VRBottom', 'VRRight']
        if all(key in info for key in view_keys):
            top = int(info['VRTop'])
            left = int(info['VRLeft'])
            bottom = int(info['VRBottom'])
            right = int(info['VRRight'])
            self.set_view_limit(left, top, right - left, bottom - top)

        # Set view boundaries using minimap
        minimap_keys = ['centerX', 'centerY', 'width', 'height']
        if all(key in minimap for key in minimap_keys) and not self.view_limit:
            x = int(minimap['centerX'])
            y = int(minimap['centerY'])
            width = int(minimap['width'])
            height = int(minimap['height'])
            self.set_view_limit(-x, -y, width, height)

        # Set view boundaries using footholds
        if foothold and not self.view_limit:
            # Get min/max foothold items
            x1 = min([min([x['x1'] for x in v]) for k, v in foothold.items()])
            y1 = min([min([x['y1'] for x in v]) for k, v in foothold.items()])
            x2 = min([min([x['x2'] for x in v]) for k, v in foothold.items()])
            y2 = min([min([x['y2'] for x in v]) for k, v in foothold.items()])
            self.set_view_limit(x1, y1, x2 - x1, y2 - y1)

        # Create mini map ui
        if 'canvas_image' in minimap:
            overlay_sprites = LayeredSpritesNx()
            overlay_sprites.load_minimap(info, minimap)
            self.overlayed_sprites = overlay_sprites

        # Bgm
        if 'bgm' in info:
            try:
                buffer = self.sound_nx.get_sound(info['bgm'])
                self.bgm.load(info['bgm'], buffer=buffer)
                self.bgm.volume(1.0)
            except:
                pass

    def setup_background_sprites(self, map_id):

        # Check if map nx is loaded
        if not self.map_nx.file:
            return

        # Load background
        background_sprites = BackgroundSpritesNx()
        background_sprites.load_background(self.map_nx, map_id)
        self.background_sprites = background_sprites

    def setup_layered_sprites(self, map_id):

        # Check if map nx is loaded
        if not self.map_nx.file:
            return

        # Load layers
        for i in range(0, 8):
            layered_sprites = LayeredSpritesNx()
            layered_sprites.load_layer(self.map_nx, map_id, i)
            self.layered_sprites.append(layered_sprites)

    def setup_portal_sprites(self, map_id):

        # Check if map nx is loaded
        if not self.map_nx.file:
            return

        # Load portals
        portal_sprites = LayeredSpritesNx()
        portal_sprites.load_portal(self.map_nx, map_id)
        self.layered_sprites.append(portal_sprites)

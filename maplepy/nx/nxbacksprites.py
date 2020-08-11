import os
import sys
import pygame

from maplepy.info.instance import Instance
from maplepy.info.canvas import Canvas
from maplepy.info.foothold import Foothold

from maplepy.nx.nxmap import NXMap
from maplepy.nx.nxspritemanager import NXSpriteManager


class NXBackSprites():

    def __init__(self):
        self.nx = NXMap()
        self.info = None
        self.sprite_manager = NXSpriteManager()
        self.sprites = pygame.sprite.LayeredUpdates()

    def load_nx(self, file):
        self.nx.open(file)
        self.sprite_manager.file = self.nx.file

    def load_map(self, map_id):

        # Check if map is available
        img = '{}.img'.format(map_id)
        if not self.nx.maps or img not in self.nx.maps:
            print('Could not load {}'.format(map_id))

        info = self.nx.get_info_data(map_id)

        background = self.nx.get_background_data(map_id)
        self.load_background(background)

    def load_background(self, values):

        # Go through instances list and add
        for val in values:

            # Build object
            inst = Instance()

            # Required properties
            inst.x = int(val['x'])
            inst.y = int(val['y'])
            inst.cx = int(val['cx'])
            inst.cy = int(val['cy'])
            inst.rx = int(val['rx'])
            inst.ry = int(val['ry'])
            inst.f = int(val['f'])
            inst.a = int(val['a'])
            inst.type = int(val['type'])
            inst.front = int(val['front'])
            inst.ani = int(val['ani'])
            inst.bS = val['bS']
            inst.no = int(val['no'])

            # Get sprite by key and index
            sprite = self.sprite_manager.get_sprite(
                'Back', inst.bS, None, 'back/{}'.format(inst.no))
            w, h = sprite.image.get_size()

            # Get additional properties
            object_data = self.nx.get_data(
                '{}/{}.img/back/{}'.format('Back', inst.bS, inst.no))
            x = object_data['origin'][0]
            y = object_data['origin'][1]
            z = int(object_data['z'])

            # Create a canvas object
            canvas = Canvas(sprite.image, w, h, x, y, z)

            # Flip
            if inst.f > 0:
                canvas.flip()

            # Check cx, cy
            if not inst.cx:
                inst.cx = w
            if not inst.cy:
                inst.cy = h

            # Add to object
            inst.add_canvas(canvas)

            # Add to list
            self.sprites.add(inst)

    def update(self):

        for sprite in self.sprites:
            sprite.update()

    def blit(self, surface, offset=None):

        for sprite in self.sprites:
            try:

                # Get rect
                rect = sprite.rect

                # Camera offset
                if offset:

                    # If the sprite is outside the surface
                    if not sprite.rect.colliderect(offset):
                        continue

                    rect = sprite.rect.move(-offset.x, -offset.y)

                # Draw
                surface.blit(sprite.image, rect)

            except:
                continue

import os
import sys
import pygame

from maplepy.info.instance import Instance
from maplepy.info.canvas import Canvas
from maplepy.info.foothold import Foothold

from maplepy.nx.nxmap import NXMap
from maplepy.nx.nxresourcemanager import NXResourceManager


class NXBackSprites():

    def __init__(self):
        self.nx = NXMap()
        self.info = None
        self.resource = NXResourceManager()
        self.sprites = pygame.sprite.LayeredUpdates()

    def load_nx(self, file):
        self.nx.open(file)

    def load_map(self, map_id):

        # Check if map is available
        img = '{}.img'.format(map_id)
        if not self.nx.maps or img not in self.nx.maps:
            print('Could not load {}'.format(map_id))

        # Set info
        info = self.nx.get_info_data(map_id)
        self.info = info

        # Load back sprites
        background = self.nx.get_background_data(map_id)
        self.load_background(background)

    def load_background(self, values):

        # Go through instances list and add
        for val in values:
            try:

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
                sprite = self.resource.get_sprite(
                    self.nx.file, 'Back', inst.bS, None, 'back/{}'.format(inst.no))
                w, h = sprite.image.get_size()

                # Get additional properties
                object_data = self.resource.get_data(
                    self.nx.file, 'Back', inst.bS, 'back', '{}'.format(inst.no))
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

            except Exception as e:
                print(e.args)
                continue

    def calculate_x(self, rx, dx, z):
        """ Calculate the camera x offset """
        return float(rx * (dx + z) / 100) + z

    def calculate_y(self, ry, dy, z):
        """ Calculate the camera y offset """
        return float(ry * (dy + z) / 100) + z

    def update(self):
        for sprite in self.sprites:
            sprite.update()

    def blit(self, surface, offset=None):

        # Get surface properties
        w, h = surface.get_size()

        # For all objects
        for sprite in self.sprites:
            try:

                # Get rect with animation offset
                rect = sprite.rect.move(sprite.dx, sprite.dy)

                # Camera offset
                dx = offset.x if offset else 0
                dy = offset.y if offset else 0
                x = self.calculate_x(sprite.rx, dx, 0.5 * w)
                y = self.calculate_y(sprite.ry, dy, 0.5 * h)
                rect = rect.move(x, y)

                # 0 - Simple image (eg. the hill with the tree in the background of Henesys)
                if sprite.type == 0:
                    surface.blit(sprite.image, rect)

                # 1 - Image is copied horizontally (eg. the sea in Lith Harbor)
                # 2 - Image is copied vertically (eg. trees in maps near Ellinia)
                # 3 - Image is copied in both directions (eg. the background sky color square in many maps)
                # 4 - Image scrolls and is copied horizontally (eg. clouds)
                # 5 - Image scrolls and is copied vertically (eg. background in the Helios Tower elevator)
                # 6 - Image scrolls horizontally, and is copied in both directions (eg. the train in Kerning City subway JQ)
                # 7 - Image scrolls vertically, and is copied in both directions (eg. rain drops in Ellin PQ maps)
                horizontal = [1, 3, 4, 6, 7]
                if sprite.type in horizontal:
                    if sprite.cx > 0:
                        tile = rect.copy()
                        while tile.x < w:
                            surface.blit(sprite.image, tile)
                            tile = tile.move(sprite.cx, 0)
                        tile = rect.copy()
                        while tile.x > -sprite.rect.width:
                            surface.blit(sprite.image, tile)
                            tile = tile.move(-sprite.cx, 0)
                vertical = [2, 3, 5, 6, 7]
                if sprite.type in vertical:
                    if sprite.cy > 0:
                        tile = rect.copy()
                        while tile.y < h:
                            surface.blit(sprite.image, tile)
                            tile = tile.move(0, sprite.cy)
                        tile = rect.copy()
                        while tile.y > -sprite.rect.height:
                            surface.blit(sprite.image, tile)
                            tile = tile.move(0, -sprite.cy)

            except:
                continue

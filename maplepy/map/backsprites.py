import os
import pygame

from maplepy.xml.basexml import Layer, BaseXml
from maplepy.info.instance import Instance
from maplepy.info.canvas import Canvas


class BackSprites():
    """ Class containing background images for the map """

    def __init__(self):
        self.xml = {}
        self.images = {}
        self.sprites = pygame.sprite.Group()

    def load_xml(self, path, name):

        # Check if xml has already been loaded before
        if name in self.xml:
            print('{} was already loaded.'.format(name))
            return

        # Load and parse the xml
        file = "{}/map.wz/Back/{}.img.xml".format(path, name)
        self.xml[name] = BaseXml()
        self.xml[name].open(file)
        self.xml[name].parse_root(Layer.CANVAS_ARRAY)

    def load_images(self, path, name):

        # Check if images have already been loaded before
        if name in self.images:
            return self.images[name]

        # Check if xml has finished loading
        if name not in self.xml or not self.xml[name].items:
            print('{} was not loaded yet.'.format(name))
            return

        # Get current xml file
        xml = self.xml[name]

        # Load images for a given xml file
        images = []
        for index in range(0, 100):  # Num images
            file = "{}/map.wz/Back/{}/back.{}.png".format(
                path, xml.name, str(index))
            if os.path.isfile(file):
                image = pygame.image.load(file).convert_alpha()
                images.append(image)
            else:
                break

        # Store images
        self.images[name] = images

        # Return
        return images

    def load_backgrounds(self, path, name, values):

        # Check if xml has finished loading
        if name not in self.xml or not self.xml[name].items:
            print('{} was not loaded yet.'.format(name))
            return

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
                images = self.images[inst.bS]
                sprite = images[inst.no]
                w, h = sprite.get_size()

                # Get additional properties
                object_data = self.xml[name].items
                back_data = object_data['back']
                data = back_data[inst.no]
                x = int(data['x'])
                y = int(data['y'])
                z = int(data['z'])

                # Create a canvas object
                canvas = Canvas(sprite, w, h, x, y, z)

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

            except:
                print('Error while loading background')
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

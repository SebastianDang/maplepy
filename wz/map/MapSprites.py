import os
import sys
import pygame

from wz.xml.BaseXml import Layer, BaseXml
from wz.info.Instance import Instance
from wz.info.Canvas import Canvas
from wz.info.Foothold import Foothold


class MapSprites():

    def __init__(self):
        self.xmls = {}
        self.images = {}
        self.sprites = pygame.sprite.LayeredUpdates()

    def load_xml(self, path, subtype, name):

        # Create key
        key = "{}/{}".format(subtype, name)

        # Check if file has already been loaded before
        if key in self.xmls:
            print('{} was already loaded.'.format(key))
            return

        # Open file
        file = "{}/map.wz/{}/{}.img.xml".format(
            path, subtype, name)
        self.xmls[key] = BaseXml()
        self.xmls[key].open(file)

        # Parse by type
        if subtype == 'Tile':
            self.xmls[key].parse_root(Layer.CANVAS_ARRAY)
        elif subtype == 'Obj':
            self.xmls[key].parse_root(Layer.TAGS)

    def load_tiles(self, path, subtype, name, values):

        # Create key
        key = "{}/{}".format(subtype, name)

        # Check if file has finished loading
        if key not in self.xmls:
            print('{} was was not loaded yet.'.format(key))
            return

        # Get images
        if key in self.images:
            tile_images = self.images[key]
        else:
            tile_images = self.load_tile_images(path, subtype, name)

        # Get xml
        xml = self.xmls[key]

        # Go through instances list and add
        for val in values:
            try:

                # Build object
                inst = Instance()

                # Required properties
                inst.x = int(val['x'])
                inst.y = int(val['y'])
                inst.u = val['u']
                inst.no = int(val['no'])
                inst.zM = int(val['zM'])

                # Get sprite by key and index
                images = tile_images[inst.u]
                image = images[inst.no]
                w, h = image.get_size()

                # Get additional properties
                item = xml.objects[inst.u][inst.no]
                x = int(item['x'])
                y = int(item['y'])
                z = int(item['z'])

                # Create a canvas object
                canvas = Canvas(image, w, h, x, y, z)

                # Add footholds
                if 'extended' in item:
                    for foothold in item['extended']:
                        fx = int(foothold['x'])
                        fy = int(foothold['y'])
                        canvas.add_foothold(Foothold(fx, fy))

                # Explicit special case
                if not inst.zM:
                    inst.update_layer(canvas.z)

                # Add to object
                inst.add_canvas(canvas)

                # Add to list
                self.sprites.add(inst)

            except:
                print('Error while loading tiles')
                continue

    def load_tile_images(self, path, subtype, name):

        # Create key
        key = "{}/{}".format(subtype, name)

        # Check if sprites are already loaded
        if key in self.images:
            return self.images[key]

        # Load sprites
        image_group = {}
        for obj in self.xmls[key].objects:
            images = []
            for index in range(0, 20):  # Max num of frames
                file = "{}/map.wz/{}/{}.img/{}.{}.png".format(
                    path, subtype, name, obj, str(index))
                if os.path.isfile(file):
                    image = pygame.image.load(file).convert_alpha()
                    images.append(image)
                else:
                    break
            image_group[obj] = images

        # Store images
        self.images[key] = image_group

        # Return
        return image_group

    def load_objects(self, path, subtype, name, values):

        # Go through instances list and add
        for val in values:
            try:

                # Build object
                inst = Instance()

                # Required properties
                inst.x = int(val['x'])
                inst.y = int(val['y'])
                inst.oS = val['oS']
                inst.l0 = val['l0']
                inst.l1 = val['l1']
                inst.l2 = val['l2']
                inst.zM = int(val['zM'])
                inst.f = int(val['f'])

                # Optional properties
                if 'r' in val:
                    inst.r = int(val['r'])
                if 'move' in val:
                    inst.move = int(val['move'])
                if 'dynamic' in val:
                    inst.dynamic = int(val['dynamic'])
                if 'piece' in val:
                    inst.piece = int(val['piece'])

                # Load sprites
                images = self.load_object_images(
                    path, subtype, inst.oS, inst.l0, inst.l1, inst.l2)

                # Create key
                key = "{}/{}".format(subtype, inst.oS)

                # Get xml
                if key not in self.xmls or not self.xmls[key].objects:
                    print('{} was not loaded yet.'.format(key))
                    continue
                xml = self.xmls[key]

                # Get additional properties
                objects = xml.objects
                l0 = objects[inst.l0]
                l1 = l0[inst.l1]
                l2 = l1[int(inst.l2)]

                # Create canvases
                for i in range(0, len(images)):

                    # Get sprite info
                    sprite = images[i]
                    w, h = sprite.get_size()

                    # Get xml info
                    item = l2[i]
                    x = int(item['x'])
                    y = int(item['y'])
                    z = int(item['z']) if 'z' in item else 0
                    delay = int(item['delay']) if 'delay' in item else 120

                    # Create a canvas object
                    canvas = Canvas(sprite, w, h, x, y, z)

                    # Set delay
                    canvas.set_delay(delay)

                    # Add footholds
                    if 'extended' in item:
                        for foothold in item['extended']:
                            fx = int(foothold['x'])
                            fy = int(foothold['y'])
                            canvas.add_foothold(Foothold(fx, fy))

                    # Flip
                    if inst.f > 0:
                        canvas.flip()

                    # Add to object
                    inst.add_canvas(canvas)

                    # Explicit special case
                    if 'z' in val:
                        inst.update_layer(int(val['z']))

                # Add to list
                self.sprites.add(inst)

            except:
                print('Error while loading objects')
                continue

    def load_object_images(self, path, subtype, name, l0, l1, l2):

        # Create key
        key = "{}/{}/{}.{}.{}".format(
            subtype, name, l0, l1, l2)

        # Check if sprites are already loaded
        if key in self.images:
            return self.images[key]

        # Get a list of images for the key
        images = []
        for index in range(0, 20):  # Num frames
            file = '{}/map.wz/{}/{}.img/{}.{}.{}.{}.png'.format(
                path, subtype, name, l0, l1, l2, str(index))
            if os.path.isfile(file):
                image = pygame.image.load(file).convert_alpha()
                images.append(image)
            else:
                break

        # Store images
        self.images[key] = images

        # Return list of images
        return images

    def update(self):

        if not self.sprites:
            return

        for sprite in self.sprites:
            sprite.step_frame()

    def blit(self, surface, offset=None):

        if not self.sprites:
            return

        for sprite in self.sprites:
            try:

                # Camera offset
                if offset:
                    rect = sprite.rect.move(-offset.x, -offset.y)

                # Draw
                surface.blit(sprite.image, rect)

            except:
                continue

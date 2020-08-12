import os
import pygame

import maplepy.display.displayitems as displayitems

from maplepy.xml.basexml import Layer, BaseXml
from maplepy.info.instance import Instance
from maplepy.info.canvas import Canvas
from maplepy.info.foothold import Foothold

# Cache individual xmls and images here
xml_cache = {}
image_cache = {}


class BackgroundSpritesXml(displayitems.BackgroundSprites):
    """ Class containing background images for the map """

    def __init__(self):

        # Create sprites
        super().__init__()

    def load_xml(self, path, name):

        # Check if xml has already been loaded before
        if name in xml_cache:
            print('{} was already loaded.'.format(name))
            return

        # Load and parse the xml
        file = "{}/map.wz/Back/{}.img.xml".format(path, name)
        xml_cache[name] = BaseXml()
        xml_cache[name].open(file)
        xml_cache[name].parse_root(Layer.CANVAS_ARRAY)

    def load_images(self, path, name):

        # Check if images have already been loaded before
        if name in image_cache:
            return image_cache[name]

        # Check if xml has finished loading
        if name not in xml_cache or not xml_cache[name].items:
            print('{} was not loaded yet.'.format(name))
            return

        # Get current xml file
        xml = xml_cache[name]

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
        image_cache[name] = images

        # Return
        return images

    def load_backgrounds(self, path, name, values):

        # Check if xml has finished loading
        if name not in xml_cache or not xml_cache[name].items:
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
                images = image_cache[inst.bS]
                sprite = images[inst.no]
                w, h = sprite.get_size()
                sprite.set_alpha(inst.a)

                # Get additional properties
                object_data = xml_cache[name].items
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


class LayeredSpritesXml(displayitems.LayeredSprites):
    """
    Class containing tile and object images for the map
    """

    def __init__(self):

        # Create sprites
        super().__init__()

    def load_xml(self, path, subtype, name):

        # Create key
        key = "{}/{}".format(subtype, name)

        # Check if file has already been loaded before
        if key in xml_cache:
            print('{} was already loaded.'.format(key))
            return

        # Open file
        file = "{}/map.wz/{}/{}.img.xml".format(
            path, subtype, name)
        xml_cache[key] = BaseXml()
        xml_cache[key].open(file)

        # Parse by type
        if subtype == 'tile':
            xml_cache[key].parse_root(Layer.CANVAS_ARRAY)
        elif subtype == 'obj':
            xml_cache[key].parse_root(Layer.TAGS)

    def load_tiles(self, path, subtype, name, values):

        # Create key
        key = "{}/{}".format(subtype, name)

        # Check if file has finished loading
        if key not in xml_cache:
            print('{} was was not loaded yet.'.format(key))
            return

        # Get images
        if key in image_cache:
            tile_images = image_cache[key]
        else:
            tile_images = self.load_tile_images(path, subtype, name)

        # Get xml
        xml = xml_cache[key]

        # Go through instances list and add
        for val in values:
            try:

                # Build object
                inst = Instance()

                # Get info
                info = val['info']
                if 'forbidFallDown' in info:
                    inst.forbidFallDown = int(info['forbidFallDown'])

                # Get name
                tag_name = val['name'] if 'name' in val else None

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
                item = xml.items[inst.u][inst.no]
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

                # !!!For tiles, use the tag name!!!
                # Explicit special case
                # if 'z' in val:
                #     inst.update_layer(int(val['z']))
                # else:
                #     inst.update_layer(inst.zM)
                if tag_name and tag_name.isdigit():
                    inst.update_layer(int(tag_name))

                # Add to object
                inst.add_canvas(canvas)

                # Add to list
                self.sprites.add(inst)

            except:
                print('Error while loading tiles')
                continue

        # Fix tiles that are overlapping
        self.fix_overlapping_sprites()

    def load_tile_images(self, path, subtype, name):

        # Create key
        key = "{}/{}".format(subtype, name)

        # Check if sprites are already loaded
        if key in image_cache:
            return image_cache[key]

        # Load sprites
        image_group = {}
        for obj in xml_cache[key].items:
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
        image_cache[key] = image_group

        # Return
        return image_group

    def fix_overlapping_sprites(self):
        """ Fix z issues with overlapping tiles and objects """
        for sprite in self.sprites:
            collisions = pygame.sprite.spritecollide(
                sprite, self.sprites, False)
            for collision in collisions:
                if sprite.canvas_list[0].z > collision.canvas_list[0].z:
                    self.sprites.change_layer(sprite, collision._layer+1)

    def load_objects(self, path, subtype, name, values):

        # Go through instances list and add
        for val in values:
            try:

                # Build object
                inst = Instance()

                # Get info
                info = val['info']
                if 'forbidFallDown' in info:
                    inst.forbidFallDown = int(info['forbidFallDown'])

                # Required properties
                inst.x = int(val['x'])
                inst.y = int(val['y'])
                inst.z = int(val['z']) if 'z' in val else None
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
                if key not in xml_cache or not xml_cache[key].items:
                    print('{} was not loaded yet.'.format(key))
                    continue
                xml = xml_cache[key]

                # Get additional properties
                objects = xml.items
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
                    a0 = int(item['a0']) if 'a0' in item else 255
                    a1 = int(item['a1']) if 'a1' in item else 255

                    # Create a canvas object
                    canvas = Canvas(sprite, w, h, x, y, z)

                    # Set delay
                    canvas.set_delay(delay)

                    # Set alphas
                    canvas.set_alpha(a0, a1)

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

                # !!!For objects, use the z value!!!
                # # Explicit special case
                if 'z' in val:
                    inst.update_layer(int(val['z']))
                else:
                    inst.update_layer(inst.zM)

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
        if key in image_cache:
            return image_cache[key]

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
        image_cache[key] = images

        # Return list of images
        return images

    def load_portals(self, path, values):

        # TODO: Remove magic numbers
        portals = {2: 'portal.game.pv.default', 8: 'portal.game.pv.5'}
        magic = {2: [(49, 134), (48, 130), (50, 123), (50, 125),
                     (50, 130), (51, 130), (49, 126), (49, 130)],
                 8: [(58, 149), (57, 154), (58, 147), (58, 147),
                     (58, 152), (58, 150), (58, 149), (58, 148),
                     (58, 151), (57, 148), (58, 154), (58, 147),
                     (59, 154), (58, 147), (58, 147), (58, 148)]}

        # Go through instances list and add
        for val in values:
            try:

                # Build object
                inst = Instance()

                # Required properties
                inst.x = int(val['x'])
                inst.y = int(val['y'])

                # Portal type
                pt = int(val['pt'])
                if pt not in portals:
                    continue

                # Check if sprites are already loaded
                key = portals[pt]
                if key not in image_cache:
                    images = []
                    for index in range(0, 20):  # Num frames
                        file = '{}/img/portals/{}.{}.png'.format(
                            '.', key, str(index))
                        if os.path.isfile(file):
                            image = pygame.image.load(file).convert_alpha()
                            images.append(image)
                        else:
                            break
                    image_cache[key] = images

                # Get sprite by key
                images = image_cache[key]

                # Create canvases
                for i in range(0, len(images)):

                    # Get sprite info
                    sprite = images[i]
                    w, h = sprite.get_size()

                    # Create a canvas object
                    data = magic[pt]
                    canvas = Canvas(sprite, w, h, data[i][0], data[i][1])
                    canvas.set_delay(100)

                    # Add to object
                    inst.add_canvas(canvas)

                # Add to list
                self.sprites.add(inst)

            except:
                print('Error while loading portals')
                continue

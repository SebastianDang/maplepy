import os
import pygame

import maplepy.display.displayitems as displayitems

from maplepy.info.instance import Instance
from maplepy.info.canvas import Canvas
from maplepy.info.foothold import Foothold

from maplepy.nx.nxresourcemanager import NXResourceManager

resource_manager = NXResourceManager()


class BackgroundSpritesNx(displayitems.BackgroundSprites):
    """ Class containing background images for the map """

    def __init__(self):

        # Create sprites
        super().__init__()

    def load_background(self, map_nx, map_id):

        # Load back sprites
        values = map_nx.get_background_data(map_id)
        if not values:
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
                sprite = resource_manager.get_sprite(
                    map_nx.file, 'Back', inst.bS, 'back', inst.no)
                w, h = sprite.image.get_size()
                sprite.image.set_alpha(inst.a)

                # Get additional properties
                object_data = resource_manager.get_data(
                    map_nx.file, 'Back', inst.bS, 'back', inst.no)
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


class LayeredSpritesNx(displayitems.LayeredSprites):
    """
    Class containing tile and object images for the map
    """

    def __init__(self):

        # Create sprites
        super().__init__()

    def load_layer(self, map_nx, map_id, index):

        values = map_nx.get_layer_data(map_id, index)
        if not values:
            return

        # Go through instances list and add
        for val in values['tile']:
            try:

                # Build object
                inst = Instance()

                # Get info
                info = values['info']
                if 'forbidFallDown' in info:
                    inst.forbidFallDown = int(info['forbidFallDown'])

                # Make sure there's tile information
                if 'tS' not in info:
                    continue

                # Get name
                tag_name = val['name'] if 'name' in val else None

                # Required properties
                inst.x = int(val['x'])
                inst.y = int(val['y'])
                inst.tS = info['tS']
                inst.u = val['u']
                inst.no = int(val['no'])
                inst.zM = int(val['zM'])

                # Get sprite by key and index
                sprite = resource_manager.get_sprite(
                    map_nx.file, 'Tile', inst.tS, inst.u, inst.no)
                w, h = sprite.image.get_size()

                # Get additional properties
                object_data = resource_manager.get_data(
                    map_nx.file, 'Tile', inst.tS, inst.u, inst.no)
                x = object_data['origin'][0]
                y = object_data['origin'][1]
                z = int(object_data['z'])

                # Create a canvas object
                canvas = Canvas(sprite.image, w, h, x, y, z)

                # Add footholds
                if 'extended' in object_data:
                    for foothold in object_data['extended']:
                        fx = int(foothold['x'])
                        fy = int(foothold['y'])
                        canvas.add_foothold(Foothold(fx, fy))

                if tag_name and tag_name.isdigit():
                    inst.update_layer(int(tag_name))

                # Add to object
                inst.add_canvas(canvas)

                # Add to list
                self.sprites.add(inst)

            except Exception as e:
                print(e.args)
                continue

        # Fix tiles that are overlapping
        self.fix_overlapping_sprites()

    def fix_overlapping_sprites(self):
        """ Fix z issues with overlapping tiles and objects """
        for sprite in self.sprites:
            collisions = pygame.sprite.spritecollide(
                sprite, self.sprites, False)
            for collision in collisions:
                if sprite.canvas_list[0].z > collision.canvas_list[0].z:
                    self.sprites.change_layer(sprite, collision._layer+1)

    # def load_objects(self, path, subtype, name, values):

    #     # Go through instances list and add
    #     for val in values:
    #         try:

    #             # Build object
    #             inst = Instance()

    #             # Get info
    #             info = val['info']
    #             if 'forbidFallDown' in info:
    #                 inst.forbidFallDown = int(info['forbidFallDown'])

    #             # Required properties
    #             inst.x = int(val['x'])
    #             inst.y = int(val['y'])
    #             inst.z = int(val['z']) if 'z' in val else None
    #             inst.oS = val['oS']
    #             inst.l0 = val['l0']
    #             inst.l1 = val['l1']
    #             inst.l2 = val['l2']
    #             inst.zM = int(val['zM'])
    #             inst.f = int(val['f'])

    #             # Optional properties
    #             if 'r' in val:
    #                 inst.r = int(val['r'])
    #             if 'move' in val:
    #                 inst.move = int(val['move'])
    #             if 'dynamic' in val:
    #                 inst.dynamic = int(val['dynamic'])
    #             if 'piece' in val:
    #                 inst.piece = int(val['piece'])

    #             # Load sprites
    #             images = self.load_object_images(
    #                 path, subtype, inst.oS, inst.l0, inst.l1, inst.l2)

    #             # Create key
    #             key = "{}/{}".format(subtype, inst.oS)

    #             # Get nx
    #             if key not in self.nxs or not self.nxs[key].items:
    #                 print('{} was not loaded yet.'.format(key))
    #                 continue
    #             nx = self.nxs[key]

    #             # Get additional properties
    #             objects = nx.items
    #             l0 = objects[inst.l0]
    #             l1 = l0[inst.l1]
    #             l2 = l1[int(inst.l2)]

    #             # Create canvases
    #             for i in range(0, len(images)):

    #                 # Get sprite info
    #                 sprite = images[i]
    #                 w, h = sprite.get_size()

    #                 # Get nx info
    #                 item = l2[i]
    #                 x = int(item['x'])
    #                 y = int(item['y'])
    #                 z = int(item['z']) if 'z' in item else 0
    #                 delay = int(item['delay']) if 'delay' in item else 120
    #                 a0 = int(item['a0']) if 'a0' in item else 255
    #                 a1 = int(item['a1']) if 'a1' in item else 255

    #                 # Create a canvas object
    #                 canvas = Canvas(sprite, w, h, x, y, z)

    #                 # Set delay
    #                 canvas.set_delay(delay)

    #                 # Set alphas
    #                 canvas.set_alpha(a0, a1)

    #                 # Add footholds
    #                 if 'extended' in item:
    #                     for foothold in item['extended']:
    #                         fx = int(foothold['x'])
    #                         fy = int(foothold['y'])
    #                         canvas.add_foothold(Foothold(fx, fy))

    #                 # Flip
    #                 if inst.f > 0:
    #                     canvas.flip()

    #                 # Add to object
    #                 inst.add_canvas(canvas)

    #             # !!!For objects, use the z value!!!
    #             # # Explicit special case
    #             if 'z' in val:
    #                 inst.update_layer(int(val['z']))
    #             else:
    #                 inst.update_layer(inst.zM)

    #             # Add to list
    #             self.sprites.add(inst)

    #         except:
    #             print('Error while loading objects')
    #             continue

import pygame

import maplepy.display.displayitems as displayitems

from maplepy.info.instance import Instance
from maplepy.info.canvas import Canvas
from maplepy.info.foothold import Foothold

from maplepy.nx.resourcemanagernx import ResourceManagerNx

# Create a single resource manager
resource_manager = ResourceManagerNx()


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

                # Get name
                tag_name = val['name'] if 'name' in val else None

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

                # Get sprites by type
                sprites = []
                if inst.ani:  # Animated
                    for index in range(0, 20):
                        name = '{}/{}'.format(inst.no, index)
                        sprite = resource_manager.get_sprite(
                            map_nx.file, 'Back', inst.bS, 'ani', name)
                        if sprite:
                            sprites.append(sprite)
                        else:
                            break
                else:  # Static
                    sprite = resource_manager.get_sprite(
                        map_nx.file, 'Back', inst.bS, 'back', inst.no)
                    if sprite:
                        sprites.append(sprite)

                # Create canvases
                for index in range(0, len(sprites)):

                    # Get sprite info
                    sprite = sprites[index]
                    w, h = sprite.image.get_size()

                    # Get additional properties
                    if inst.ani:
                        name = '{}/{}'.format(inst.no, index)
                        data = resource_manager.get_data(
                            map_nx.file, 'Back', inst.bS, 'ani', name)
                    else:
                        data = resource_manager.get_data(
                            map_nx.file, 'Back', inst.bS, 'back', inst.no)

                    x = data['origin'][0]
                    y = data['origin'][1]
                    z = int(data['z']) if 'z' in data else None
                    delay = int(data['delay']) if 'delay' in data else 120

                    # Create a canvas object
                    canvas = Canvas(sprite.image, w, h, x, y, z)

                    # Set delay
                    canvas.set_delay(delay)

                    # Flip
                    if inst.f > 0:
                        canvas.flip()

                    # Check cx, cy
                    if not inst.cx:
                        inst.cx = w
                    if not inst.cy:
                        inst.cy = h

                    # Explicit special case
                    if tag_name and tag_name.isdigit():
                        inst.update_layer(int(tag_name))

                    # Add to object
                    inst.add_canvas(canvas)

                # Add to list
                self.sprites.add(inst)

            except:
                continue


class LayeredSpritesNx(displayitems.LayeredSprites):
    """
    Class containing tile and object images for the map
    """

    def __init__(self):

        # Create sprites
        super().__init__()

    def load_layer(self, map_nx, map_id, index):

        # Load current layer
        values = map_nx.get_layer_data(map_id, index)
        if not values:
            return

        # Get info
        info = values['info']

        # Go through instances list and add
        for val in values['tile']:
            try:

                # Make sure there's tile information
                if 'tS' not in info:
                    break

                # Build object
                inst = Instance()

                # Get any extra info
                if 'forbidFallDown' in info:
                    inst.forbidFallDown = int(info['forbidFallDown'])

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
                data = resource_manager.get_data(
                    map_nx.file, 'Tile', inst.tS, inst.u, inst.no)
                x = data['origin'][0]
                y = data['origin'][1]
                z = int(data['z']) if 'z' in data else None

                # Create a canvas object
                canvas = Canvas(sprite.image, w, h, x, y, z)

                # Explicit special case
                if tag_name and tag_name.isdigit():
                    inst.update_layer(int(tag_name))

                # Add to object
                inst.add_canvas(canvas)

                # Add to list
                self.sprites.add(inst)

            except:
                continue

        # Fix overlapping tiles
        self.fix_overlapping_sprites()

        # Go through instances list and add
        for val in values['obj']:
            try:

                # Build object
                inst = Instance()

                # Get any extra info
                if 'forbidFallDown' in info:
                    inst.forbidFallDown = int(info['forbidFallDown'])

                # Get name
                tag_name = val['name'] if 'name' in val else None

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
                sprites = []
                for index in range(0, 20):  # Num frames
                    name = '{}/{}/{}'.format(inst.l1, inst.l2, index)
                    sprite = resource_manager.get_sprite(
                        map_nx.file, 'Obj', inst.oS, inst.l0, name)
                    if sprite:
                        sprites.append(sprite)
                    else:
                        break

                # Create canvases
                for index in range(0, len(sprites)):

                    # Get sprite info
                    sprite = sprites[index]
                    w, h = sprite.image.get_size()

                    # Get additional properties
                    name = '{}/{}/{}'.format(inst.l1, inst.l2, index)
                    data = resource_manager.get_data(
                        map_nx.file, 'Obj', inst.oS, inst.l0, name)
                    x = data['origin'][0]
                    y = data['origin'][1]
                    z = int(data['z']) if 'z' in data else None
                    delay = int(data['delay']) if 'delay' in data else 120
                    a0 = int(data['a0']) if 'a0' in data else 255
                    a1 = int(data['a1']) if 'a1' in data else 255

                    # Create a canvas object
                    canvas = Canvas(sprite.image, w, h, x, y, z)

                    # Set delay
                    canvas.set_delay(delay)

                    # Set alphas
                    canvas.set_alpha(a0, a1)

                    # Flip
                    if inst.f > 0:
                        canvas.flip()

                    # Add to object
                    inst.add_canvas(canvas)

                # Explicit special case
                if 'z' in val:
                    inst.update_layer(int(val['z']))
                else:
                    inst.update_layer(inst.zM)

                # Add to list
                self.sprites.add(inst)

            except:
                continue

    def fix_overlapping_sprites(self):
        """ Fix z issues with overlapping tiles and objects """
        for sprite in self.sprites:
            collisions = pygame.sprite.spritecollide(
                sprite, self.sprites, False)
            for collision in collisions:
                if sprite.canvas_list[0].z > collision.canvas_list[0].z:
                    self.sprites.change_layer(sprite, collision._layer+1)

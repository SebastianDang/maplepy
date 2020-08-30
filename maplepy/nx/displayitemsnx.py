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

                # Extract properties
                inst = Instance()
                for k, v in val.items():
                    setattr(inst, k, v)

                # Build canvases
                for index in range(20):

                    # Get sprite
                    if inst.ani:  # Animated
                        subtype = 'ani'
                        no = '{}/{}'.format(inst.no, index)
                    else:  # Static
                        subtype = 'back'
                        no = str(inst.no)
                    sprite = resource_manager.get_sprite(
                        map_nx.file, 'Back', inst.bS, subtype, no)

                    # Sprite not found
                    if not sprite:
                        break

                    # Get info
                    w, h = sprite.image.get_size()
                    data = resource_manager.get_data(
                        map_nx.file, 'Back', inst.bS, subtype, no)

                    x = data['origin'][0]
                    y = data['origin'][1]
                    z = int(data['z']) if 'z' in data else None
                    delay = int(data['delay']) if 'delay' in data else 120

                    # Create a canvas object
                    canvas = Canvas(sprite.image, w, h, x, y, z)

                    # Flip
                    if inst.f and inst.f > 0:
                        canvas.flip()

                    # Check cx, cy
                    if not inst.cx:
                        inst.cx = w
                    if not inst.cy:
                        inst.cy = h

                    # Set delay
                    canvas.set_delay(delay)

                    # Add to object
                    inst.add_canvas(canvas)

                    # Do not continue if static
                    if not inst.ani:
                        break

                # Explicit special case
                if inst.name and inst.name.isdigit():
                    inst.update_layer(int(inst.name))

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

                # Extract properties
                inst = Instance()
                inst.tS = info['tS']
                for k, v in val.items():
                    setattr(inst, k, v)

                # Get sprite
                sprite = resource_manager.get_sprite(
                    map_nx.file, 'Tile', inst.tS, inst.u, str(inst.no))

                # Sprite not found
                if not sprite:
                    break

                # Get info
                w, h = sprite.image.get_size()
                data = resource_manager.get_data(
                    map_nx.file, 'Tile', inst.tS, inst.u, str(inst.no))

                x = data['origin'][0]
                y = data['origin'][1]
                z = int(data['z']) if 'z' in data else None

                # Create a canvas object
                canvas = Canvas(sprite.image, w, h, x, y, z)

                # Add to object
                inst.add_canvas(canvas)

                # Explicit special case
                if inst.name and inst.name.isdigit():
                    inst.update_layer(int(inst.name))

                # Add to list
                self.sprites.add(inst)

            except:
                continue

        # Fix overlapping tiles
        self.fix_overlapping_sprites()

        # Go through instances list and add
        for val in values['obj']:
            try:

                # Extract properties
                inst = Instance()
                for k, v in val.items():
                    setattr(inst, k, v)

                # Build canvases
                for index in range(20):

                    # Get sprite
                    no = '{}/{}/{}'.format(inst.l1, inst.l2, index)
                    sprite = resource_manager.get_sprite(
                        map_nx.file, 'Obj', inst.oS, inst.l0, no)

                    # Sprite not found
                    if not sprite:
                        break

                    # Get info
                    w, h = sprite.image.get_size()
                    data = resource_manager.get_data(
                        map_nx.file, 'Obj', inst.oS, inst.l0, no)

                    x = data['origin'][0]
                    y = data['origin'][1]
                    z = int(data['z']) if 'z' in data else None
                    delay = int(data['delay']) if 'delay' in data else 120
                    a0 = int(data['a0']) if 'a0' in data else 255
                    a1 = int(data['a1']) if 'a1' in data else 255

                    # Create a canvas object
                    canvas = Canvas(sprite.image, w, h, x, y, z)

                    # Flip
                    if inst.f and inst.f > 0:
                        canvas.flip()

                    # Set delay
                    canvas.set_delay(delay)

                    # Set alphas
                    canvas.set_alpha(a0, a1)

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

        # Load portal list
        values = map_nx.get_portal_data(map_id)
        if not values:
            return

        # Visible portal types
        visible_portals = [2, 7]

        # Go through portal list and add
        for val in values:
            try:

                # Extract properties
                inst = Instance()
                for k, v in val.items():
                    setattr(inst, k, v)

                # Check visibility
                if inst.pt not in visible_portals:
                    continue

                # Build canvases
                for index in range(20):

                    # Get sprite
                    no = 'pv/default/{}'.format(index)
                    sprite = resource_manager.get_sprite(
                        map_nx.file, None, 'MapHelper', 'portal/game', no)

                    # Sprite not found
                    if not sprite:
                        break

                    # Get info
                    w, h = sprite.image.get_size()
                    data = resource_manager.get_data(
                        map_nx.file, None, 'MapHelper', 'portal/game', no)

                    x = data['origin'][0]
                    y = data['origin'][1]
                    z = int(data['z']) if 'z' in data else None

                    # Create a canvas object
                    canvas = Canvas(sprite.image, w, h, x, y, z)

                    # Set delay
                    canvas.set_delay(100)

                    # Set alphas
                    canvas.set_alpha(80, 80)

                    # Add to object
                    inst.add_canvas(canvas)

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

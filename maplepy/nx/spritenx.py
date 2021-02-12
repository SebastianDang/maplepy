import logging

import pygame
from maplepy.base.sprite import BackgroundSprites, LayeredSprites
from maplepy.info.canvas import Canvas
from maplepy.info.instance import Instance
from maplepy.nx.resourcenx import ResourceNx

# Create a single resource manager
resource_manager = ResourceNx()


class BackgroundSpritesNx(BackgroundSprites):
    """ Class containing background images for the map """

    def __init__(self):

        # Create sprites
        super().__init__()

    def load_background(self, map_nx, map_id):

        # Load back sprites
        values = map_nx.get_back(map_id)
        if not values:
            logging.warning('Background data not found')
            return

        # Go through instances list and add
        for val in values:
            try:

                # Extract properties
                inst = Instance()
                for k, v in val.items():
                    setattr(inst, k, v)

                # Get node
                subtype = 'ani' if inst.ani else 'back'
                key = f'Back/{inst.bS}.img/{subtype}/{inst.no}'
                node = map_nx.file.resolve(key)
                count = node.child_count if node and inst.ani else 1

                # Build canvases
                for index in range(count):

                    # Get data
                    if inst.ani:  # Animated
                        # subtype = 'ani'
                        no = f'{inst.no}/{index}'
                    else:  # Static
                        # subtype = 'back'
                        no = str(inst.no)
                    sprite = resource_manager.get_sprite(
                        map_nx.file, 'Back', inst.bS, subtype, no)
                    data = resource_manager.get_data(
                        map_nx.file, 'Back', inst.bS, subtype, no)

                    # Data not found
                    if not sprite or not data:
                        break

                    # Get info
                    w, h = sprite.image.get_size()
                    x = data['origin'][0] if 'origin' in data else 0
                    y = data['origin'][1] if 'origin' in data else 0
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
                if inst.canvas_list:
                    self.sprites.add(inst)

            except:
                logging.exception('Failed to load background')
                continue


class LayeredSpritesNx(LayeredSprites):
    """
    Class containing tile and object images for the map
    """

    def __init__(self):

        # Create sprites
        super().__init__()

    def load_minimap(self, info, val):

        # Translate
        val['x'] = 0
        val['y'] = 0

        # Extract properties
        inst = Instance()
        for k, v in val.items():
            setattr(inst, k, v)

        # Get data
        key = info['mapMark']
        sprite = resource_manager.add_sprite(f'{key}', inst.canvas_image)

        # Build canvas
        w = inst.width >> inst.mag
        h = inst.height >> inst.mag
        canvas = Canvas(sprite.image, w, h)

        # Add to object
        inst.add_canvas(canvas)

        # Add to list
        if inst.canvas_list:
            self.sprites.add(inst)

    def load_layer(self, map_nx, map_id, index):

        # Load current layer
        values = map_nx.get_layer(map_id, index)
        if not values:
            logging.warning('Layer data not found')
            return

        # Get info
        info = values['info']

        # Go through instances list and add
        for val in values['tile']:
            try:

                # Make sure there's tile information
                if 'tS' not in info:
                    logging.warning('Tile data not found')
                    break

                # Extract properties
                inst = Instance()
                inst.tS = info['tS']
                for k, v in val.items():
                    setattr(inst, k, v)

                # Get Data
                sprite = resource_manager.get_sprite(
                    map_nx.file, 'Tile', inst.tS, inst.u, str(inst.no))
                data = resource_manager.get_data(
                    map_nx.file, 'Tile', inst.tS, inst.u, str(inst.no))

                # Data not found
                if not sprite or not data:
                    continue

                # Get info
                w, h = sprite.image.get_size()
                x = data['origin'][0] if 'origin' in data else 0
                y = data['origin'][1] if 'origin' in data else 0
                z = int(data['z']) if 'z' in data else None

                # Create a canvas object
                canvas = Canvas(sprite.image, w, h, x, y, z)

                # Add to object
                inst.add_canvas(canvas)

                # Explicit special case
                if inst.name and inst.name.isdigit():
                    inst.update_layer(int(inst.name))

                # Add to list
                if inst.canvas_list:
                    self.sprites.add(inst)

            except:
                logging.exception('Failed to load tile')
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

                # Get node
                key = f'Obj/{inst.oS}.img/{inst.l0}/{inst.l1}/{inst.l2}'
                node = map_nx.file.resolve(key)
                count = node.child_count

                # Build canvases
                for index in range(count):

                    # Get data
                    no = f'{inst.l1}/{inst.l2}/{index}'
                    sprite = resource_manager.get_sprite(
                        map_nx.file, 'Obj', inst.oS, inst.l0, no)
                    data = resource_manager.get_data(
                        map_nx.file, 'Obj', inst.oS, inst.l0, no)

                    # Data not found
                    if not sprite or not data:
                        break

                    # Get info
                    w, h = sprite.image.get_size()
                    x = data['origin'][0] if 'origin' in data else 0
                    y = data['origin'][1] if 'origin' in data else 0
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
                if inst.canvas_list:
                    self.sprites.add(inst)

            except:
                logging.exception('Failed to load object')
                continue

    def load_portal(self, map_nx, map_id):

        # Load portal list
        values = map_nx.get_portal(map_id)
        if not values:
            logging.warning('Portal data not found')
            return

        # Hard code some known portal stuff here
        portal_game = {2: 'pv', 7: 'pv'}

        # Go through portal list and add
        for val in values:
            try:

                # Special case
                val['pS'] = val.pop('image') if 'image' in val else 'default'

                # Extract properties
                inst = Instance()
                for k, v in val.items():
                    setattr(inst, k, v)

                # For now, only deal with in game portals
                if inst.pt not in portal_game.keys():
                    continue

                # Get node
                key = f'MapHelper.img/portal/game/{portal_game[inst.pt]}/{inst.pS}'
                node = map_nx.file.resolve(key)
                count = node.child_count

                # Build canvases
                for index in range(count):

                    # Get data
                    pt = portal_game[inst.pt]
                    no = f'game/{pt}/{inst.pS}/{index}'
                    sprite = resource_manager.get_sprite(
                        map_nx.file, None, 'MapHelper', 'portal', no)
                    data = resource_manager.get_data(
                        map_nx.file, None, 'MapHelper', 'portal', no)

                    # Data not found
                    if not sprite or not data:
                        break

                    # Get info
                    w, h = sprite.image.get_size()
                    x = data['origin'][0] if 'origin' in data else 0
                    y = data['origin'][1] if 'origin' in data else 0
                    z = int(data['z']) if 'z' in data else None

                    # Create a canvas object
                    canvas = Canvas(sprite.image, w, h, x, y, z)

                    # Set delay
                    canvas.set_delay(100)

                    # Add to object
                    inst.add_canvas(canvas)

                # Add to list
                if inst.canvas_list:
                    self.sprites.add(inst)

            except:
                logging.exception('Failed to load portal')
                continue

    def fix_overlapping_sprites(self):
        """ Fix z issues with overlapping tiles and objects """
        for sprite in self.sprites:
            collisions = pygame.sprite.spritecollide(
                sprite, self.sprites, False)
            for collision in collisions:
                if sprite.canvas_list[0].z > collision.canvas_list[0].z:
                    self.sprites.change_layer(sprite, collision._layer+1)

import logging

import pygame
from maplepy.base.sprite import BackgroundSprites, LayeredSprites
from maplepy.info.canvas import Canvas
from maplepy.info.instance import Instance
from maplepy.nx.resourcenx import ResourceNx

# Create a single resource manager
resource_manager = ResourceNx()


def create_canvas(sprite, data, delay=None, f=None):
    """ Create a canvas object from node data """

    # Missing information
    if not sprite or not data:
        return None

    # Extract basic information
    w, h = sprite.image.get_size()
    x = data['origin'][0] if 'origin' in data else 0
    y = data['origin'][1] if 'origin' in data else 0
    z = int(data['z']) if 'z' in data else None

    # Create a canvas object
    canvas = Canvas(sprite.image, w, h, x, y, z)

    # Set delay
    if delay:
        canvas.set_delay(int(data['delay']) if 'delay' in data else delay)

    # Adjustments
    if f and f > 0:
        canvas.flip()

    # Set alpha
    a0 = int(data['a0']) if 'a0' in data else 255
    a1 = int(data['a1']) if 'a1' in data else 255
    canvas.set_alpha(a0, a1)

    return canvas


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

                # Node not found
                if not node:
                    continue

                # Get children
                # count = node.child_count if node and inst.ani else 1
                if inst.ani:
                    indexes = [c for c in node.list_children()
                               if c.isnumeric()]
                else:
                    indexes = ['0']

                # Build canvases
                for index in indexes:  # range(count):

                    # Get data
                    link = f'{key}/{index}' if inst.ani else key
                    sprite = resource_manager.get_sprite(map_nx.file, link)
                    data = resource_manager.get_data(map_nx.file, link)
                    canvas = create_canvas(sprite, data, delay=120, f=inst.f)

                    # Add to object
                    inst.add_canvas(canvas)

                    # Check cx, cy
                    if not inst.cx:
                        inst.cx = canvas.width
                    if not inst.cy:
                        inst.cy = canvas.height

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
        sprite = resource_manager.cache_sprite(f'{key}', inst.canvas_image)

        # Build canvas
        w = inst.width >> inst.mag
        h = inst.height >> inst.mag
        canvas = Canvas(sprite.image, w, h)

        # Add to object
        inst.add_canvas(canvas)

        # Add to list
        if inst.canvas_list:
            self.sprites.add(inst)

    def load_layer(self, map_nx, map_id, layer):

        # Load current layer
        values = map_nx.get_layer(map_id, layer)
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

                # Get data
                link = f'Tile/{inst.tS}.img/{inst.u}/{inst.no}'
                sprite = resource_manager.get_sprite(map_nx.file, link)
                data = resource_manager.get_data(map_nx.file, link)
                canvas = create_canvas(sprite, data)

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

                # Node not found
                if not node:
                    continue

                # Get children
                indexes = [c for c in node.list_children() if c.isnumeric()]

                # Build canvases
                for index in indexes:  # range(node.child_count):

                    # Get data
                    link = f'{key}/{index}'
                    sprite = resource_manager.get_sprite(map_nx.file, link)
                    data = resource_manager.get_data(map_nx.file, link)
                    canvas = create_canvas(sprite, data, delay=120, f=inst.f)

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
        portal_game = {2: 'pv', 7: 'pv', 10: 'ph'}

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
                if inst.pt in portal_game.keys():
                    pt = portal_game[inst.pt]
                    pS = inst.pS if pt == 'pv' else 'default/portalContinue'
                else:
                    continue

                # Get node
                key = f'MapHelper.img/portal/game/{pt}/{pS}'
                node = map_nx.file.resolve(key)

                # Node not found
                if not node:
                    continue

                # Get children
                indexes = [c for c in node.list_children() if c.isnumeric()]

                # Build canvases
                for index in indexes:  # range(node.child_count):

                    # Get data
                    link = f'{key}/{index}'
                    sprite = resource_manager.get_sprite(map_nx.file, link)
                    data = resource_manager.get_data(map_nx.file, link)
                    canvas = create_canvas(sprite, data, delay=100)

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

            # Check if z exists
            if not sprite.canvas_list[0].z:
                continue

            # Collision check
            for collision in pygame.sprite.spritecollide(sprite, self.sprites, False):

                # Check if z exists
                if not collision.canvas_list[0].z:
                    continue

                if sprite.canvas_list[0].z > collision.canvas_list[0].z:
                    self.sprites.change_layer(sprite, collision._layer+1)

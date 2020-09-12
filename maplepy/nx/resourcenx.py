import logging

from maplepy.nx.spritenx import SpriteNx


class ResourceNx():
    """ Helper class to manage nx data. Load once, then store as cache """

    def __init__(self):

        self.data = {}
        self.sprites = {}

    def get_data(self, file, category, folder, subtype, name):
        """ Returns the node's values """

        # Create key
        folder += '.img'
        key = '/'.join([x for x in [category, folder, subtype, name] if x])
        # key = f'{category}/{folder}.img/{subtype}/{name}'

        # Check if data is already loaded
        if key in self.data:
            return self.data[key]

        # Check if nx is loaded yet
        if not file:
            logging.warning('Nx file is invalid')
            return None

        data = {}

        # Load from nx
        node = file.resolve(key)
        if not node:
            logging.warning(f'{key} not found')
            return None

        # Parse into dictionary
        for child in node.get_children():
            if hasattr(child, 'value'):
                data[child.name] = child.value

        # Store and return
        self.data[name] = data
        return data

    def get_sprite(self, file, category, folder, subtype, name):
        """ Returns the node's sprite """

        # Create key
        folder += '.img'
        key = '/'.join([x for x in [category, folder, subtype, name] if x])
        # key = f'{category}/{folder}.img/{subtype}/{name}'

        # Check if sprite is already loaded
        if key in self.sprites:
            return self.sprites[key]

        # Check if nx is loaded yet
        if not file:
            logging.warning('Nx file is invalid')
            return None

        # Get node
        node = file.resolve(key)
        if not node:
            logging.warning(f'{key} not found')
            return None

        # Get image
        image = node.get_image()
        if not image:
            logging.warning(f'{key} is not a sprite')
            return None

        return self.add_sprite(key, image)

    def add_sprite(self, key, image):
        """ Loads data into a sprite object, then stores it in the cache """

        # Load as nx sprite
        sprite = SpriteNx()
        sprite.load(image.width, image.height, image.get_data())

        # Store and return
        self.sprites[key] = sprite
        return sprite

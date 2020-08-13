from maplepy.nx.nxsprite import NXSprite


class NXResourceManager():
    """ Helper class to manage nx data. Load once, then store as cache """

    def __init__(self):

        self.data = {}
        self.sprites = {}

    def get_data(self, file, category, folder, subtype, name):

        # Create key
        key = '{}/{}.img/{}/{}'.format(category, folder, subtype, name)

        # Check if data is already loaded
        if key in self.data:
            return self.data[key]

        # Check if nx is loaded yet
        if not file:
            # print('Nx file is invalid')
            return None

        data = {}

        # Load from nx
        node = file.resolve(key)
        if not node:
            # print('Unable to load {}'.format(key))
            return None

        # Parse into dictionary
        for child in node.getChildren():
            if hasattr(child, 'value'):
                data[child.name] = child.value

        # Store and return
        self.data[name] = data
        return data

    def get_sprite(self, file, category, folder, subtype, name):

        # Create key
        key = '{}/{}.img/{}/{}'.format(category, folder, subtype, name)

        # Check if sprite is already loaded
        if key in self.sprites:
            return self.sprites[key]

        # Check if nx is loaded yet
        if not file:
            # print('Nx file is invalid')
            return None

        # Load from nx
        node = file.resolve(key)
        if not node:
            # print('Unable to load {}'.format(key))
            return None

        # Load as nx sprite
        image = node.getImage()
        sprite = NXSprite()
        sprite.load(image.width, image.height, image.getData())

        # Store and return
        self.sprites[key] = sprite
        return sprite

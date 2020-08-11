from maplepy.nx.nxsprite import NXSprite


class NXSpriteManager():
    """ Helper class to manage pygame sprites. Load once, then store as cache """

    def __init__(self):

        self.file = None
        self.sprites = {}

    def get_sprite(self, category, folder, subtype, name):

        # Create key
        if not subtype:
            key = '{}/{}.img/{}'.format(category, folder, name)
        else:
            key = '{}/{}.img/{}/{}'.format(category, folder, subtype, name)

        # Check if sprite is already loaded
        if key in self.sprites:
            return self.sprites[key]

        # Check if nx is loaded yet
        if not self.file:
            print('Nx file not loaded')
            return None

        # Load from nx
        node = self.file.resolve(key)
        if not node:
            print('Unable to load {}'.format(key))
            return None

        # Load as nx sprite
        byte = node.getImage()
        sprite = NXSprite()
        sprite.load(node.width, node.height, byte)

        # Store and return
        self.sprites[key] = sprite
        return sprite

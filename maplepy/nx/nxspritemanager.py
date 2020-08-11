from maplepy.nx.nxsprite import NXSprite


class NXSpriteManager():
    def __init__(self):
        self.nx = None
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
        if not self.nx:
            print('Nx file not loaded')
            return None

        # Load from nx
        node = self.nx.resolve(key)
        if not node:
            print('Unable to load {}'.format(key))
        byte = node.getImage()
        sprite = NXSprite()
        sprite.load(node.width, node.height, byte)
        self.sprites[key] = sprite
        return sprite

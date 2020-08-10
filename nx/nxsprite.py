import pygame


class nxsprite(pygame.sprite.Sprite):
    def __init__(self):

        # pygame.sprite.Sprite
        super().__init__()
        self.image = None
        self.rect = None

        # nx byte data
        self.width = 0
        self.height = 0
        self.data = []

    def load(self, w, h, data):

        # Create a new image
        image = pygame.Surface((w, h))

        # Create pixel array to access x,y coordinates
        pxarray = pygame.PixelArray(image)
        for y in range(0, h):
            for x in range(0, w):
                b = data[(y*w*4) + (x*4) + 0]
                g = data[(y*w*4) + (x*4) + 1]
                r = data[(y*w*4) + (x*4) + 2]
                a = data[(y*w*4) + (x*4) + 3]
                pxarray[x, y] = (r, g, b, a)

        # pixel array must be deleted to 'unlock' the image
        del pxarray

        # Call unlock, to be safe
        image.unlock()

        # Update current sprite
        self.image = image
        self.rect = image.get_rect()

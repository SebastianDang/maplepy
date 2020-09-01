import logging
import pygame


class SpriteNx(pygame.sprite.Sprite):
    """ Helper class to load byte array images as pygame sprites """

    def __init__(self):

        # pygame.sprite.Sprite
        super().__init__()
        self.image = None
        self.rect = None
        self.mask = None

        # nx byte data
        self.width = 0
        self.height = 0
        self.data = []

    def load(self, w, h, data):
        """
        Load image from byte array

        Each pixel is 4 bytes (32-bit) represented by:

            b   g   r   a

        Pygame stores image data as 4 bytes (32-bit) represented by:

            r   g   b   a

        Args:
            w (int): target image width
            h (int): target image height
            data (array[int]): byte array
        """
        try:

            # Create a new image
            image = pygame.Surface((w, h), pygame.SRCALPHA)
            # image.set_colorkey((0, 0, 0, 0))  # Transparent

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
            self.image = image.convert_alpha()
            self.rect = image.get_rect()
            self.mask = pygame.mask.from_surface(image)
            self.width = w
            self.height = h
            self.data = data

        except:
            logging.exception('Unable to load image')

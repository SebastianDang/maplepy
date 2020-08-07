import pygame


class Canvas(pygame.sprite.Sprite):
    """Class contains a single image, center coordinate, and footholds"""

    def __init__(self, image, w, h, x=0, y=0):

        # Sprite
        self.image = image
        self.rect = image.get_rect()
        self._layer = 0

        # Info
        self.width = w
        self.height = h
        self.x = x
        self.y = y
        self.delay = 0
        self.footholds = []

    def set_layer(self, z):
        self._layer = z

    def get_layer(self):
        return self._layer

    def get_image(self, f=0):
        if f:
            return pygame.transform.flip(self.image, True, False)
        else:
            return self.image

    def get_center_rect(self, x=0, y=0):

        # TODO: Set to True to use image instead
        use_image = False

        # Use image rect
        if use_image:
            rect = self.image.get_rect().copy()
            rect.topleft = (-self.x, -self.y)
        else:
            rect = pygame.Rect(-self.x, -self.y, self.width, self.height)

        # Adjust position
        rect = rect.move(x, y)

        # Return
        return rect

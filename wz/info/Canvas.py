import pygame


class Canvas(pygame.sprite.Sprite):
    """
    Class contains a single image and footholds.

    The constructor will automatically center the image.

    Note:
            Set the variables in this canvas once.
            This canvas should remain static after that.
            Use functions to update this canvas.

    """

    def __init__(self, image, w, h, x=0, y=0, z=0):

        # pygame.sprite.Sprite
        super().__init__()
        self.image = image
        self.rect = image.get_rect()

        # Properties
        self.width = w
        self.height = h
        self.x = x
        self.y = y
        self.z = z
        self.delay = 0
        self.footholds = []

        # Update center
        self.rect.topleft = (-self.x, -self.y)

    def set_delay(self, delay):
        self.delay = delay

    def add_foothold(self, foothold):
        self.footholds.append(foothold)

    def flip(self):
        self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        pass

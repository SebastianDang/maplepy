import pygame


class Canvas(pygame.sprite.Sprite):
    """
    Class contains a single image and additional properties
    for animation.

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

        # Animation
        self.delay = 0  # Frame duration
        self.a0 = 255  # Alpha for first frame [0,255]
        self.a1 = 255  # Alpha for last frame [0,255]

        # Update center
        self.rect.topleft = (-self.x, -self.y)

    def set_delay(self, delay):
        self.delay = delay

    def set_alpha(self, a0, a1):
        self.a0 = a0
        self.a1 = a1

    def flip(self):
        self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        pass

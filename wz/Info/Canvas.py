import pygame


class Canvas:
    def __init__(self, image, w, h, x=0, y=0, z=0):
        self.name = 'Canvas'
        self.image = image
        self.width = w
        self.height = h
        self.x = x
        self.y = y
        self.z = z
        self.footholds = []

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

import pygame

SQUARE_DELTA = 1
SQUARE_SIZE = (50, 50)
SQUARE_COLOR = (255, 0, 0)


class Square(pygame.sprite.Sprite):

    def __init__(self):

        # pygame.sprite.Sprite
        super().__init__()
        self.image = pygame.surface.Surface(SQUARE_SIZE)
        self.image.fill(SQUARE_COLOR)
        self.rect = self.image.get_rect()

    def place(self, x, y):
        self.rect.center = (x, y)

    def on_left(self):
        self.rect = self.rect.move(-SQUARE_DELTA, 0)

    def on_right(self):
        self.rect = self.rect.move(SQUARE_DELTA, 0)

    def on_up(self):
        self.rect = self.rect.move(0, -SQUARE_DELTA)

    def on_down(self):
        self.rect = self.rect.move(0, SQUARE_DELTA)

    def blit(self, surface, offset=None):

        # Check for image
        if not self.image:
            return

        # Get rect
        rect = self.rect

        # Camera offset
        if offset:

            # If the sprite is outside the surface
            if not self.rect.colliderect(offset):
                return

            rect = self.rect.move(-offset.x, -offset.y)

        # Draw
        surface.blit(self.image, rect)

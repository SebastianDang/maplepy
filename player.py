import pygame

vec = pygame.math.Vector2

MAX_VELOCITY = 5


class Player (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.surf = pygame.Surface((30, 30))
        self.surf.fill((128, 255, 40))
        self.rect = self.surf.get_rect()

        self.pos = vec(10, 380)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.dec = vec(0, 0)
        self.dir = vec(0, 0)

    def left(self):
        self.acc.x = -0.5
        self.dec.x = 0.1
        self.dir.x = -1

    def right(self):
        self.acc.x = 0.5
        self.dec.x = -0.1
        self.dir.x = 1

    def update(self):

        # Update acceleration
        self.acc += self.dec

        # Update velocity
        self.vel += self.acc

        # Limit velocity
        if self.vel.length() > MAX_VELOCITY:
            self.vel.scale_to_length(MAX_VELOCITY)

        # Verify velocity in all directions
        if self.dir.x < 0 and self.vel.x > 0:
            self.acc.x = 0
            self.dec.x = 0
            self.vel.x = 0
            self.dir.x = 0
        if self.dir.x > 0 and self.vel.x < 0:
            self.acc.x = 0
            self.dec.x = 0
            self.vel.x = 0
            self.dir.x = 0

        # Update position
        self.pos += self.vel
        self.rect.midbottom = self.pos

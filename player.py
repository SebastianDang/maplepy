import pygame

vec = pygame.math.Vector2

MAX_VELOCITY = 5


class Player (pygame.sprite.Sprite):
    def __init__(self, screen):

        super().__init__()

        self.screen = screen

        # Movement variables
        self.pos = vec(10, 380)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.dec = vec(0, 0)
        self.dir = vec(-1, 0)  # Start facing left, since the sprites face left

        # Jumping variables
        self.jumping = False
        self.jumping_pos = vec(0, 0)

        # Frame rate from screen
        self.frame_count = 0

        # Sprites
        self.stand_sprites = []
        for i in range(0, 4):
            image = pygame.image.load(
                './data/sprites/player/{}_{}.png'.format('stand1', str(i)))
            self.stand_sprites.append(image)

        self.walk_sprites = []
        for i in range(0, 4):
            image = pygame.image.load(
                './data/sprites/player/{}_{}.png'.format('walk1', str(i)))
            self.walk_sprites.append(image)

        self.jump_sprites = []
        for i in range(0, 2):
            image = pygame.image.load(
                './data/sprites/player/{}_{}.png'.format('jump', str(i)))
            self.jump_sprites.append(image)

        self.image = self.stand_sprites[0]
        self.rect = self.image.get_rect()

    def left(self):
        self.acc.x = -2.0
        self.dec.x = 0.25
        self.dir.x = -1

    def right(self):
        self.acc.x = 2.0
        self.dec.x = -0.25
        self.dir.x = 1

    def jump(self):
        if self.jumping:
            return
        self.acc.y = -5.0
        self.dec.y = 0.4
        self.jumping = True
        self.jumping_pos.x = self.pos.x
        self.jumping_pos.y = self.pos.y

    def update(self):

        # Update acceleration
        self.acc += self.dec

        # Update velocity
        self.vel += self.acc

        # Limit velocity
        if self.vel.length() > MAX_VELOCITY:
            self.vel.scale_to_length(MAX_VELOCITY)

        # Update velocity if stopped
        if self.dir.x < 0 and self.vel.x > 0:
            self.vel.x = 0
            self.acc.x = 0
            self.dec.x = 0
        if self.dir.x > 0 and self.vel.x < 0:
            self.vel.x = 0
            self.acc.x = 0
            self.dec.x = 0

        # Update position
        self.pos += self.vel

        # Check jumps
        if self.jumping:
            if self.pos.y < (self.jumping_pos.y - 50):
                self.pos.y = self.jumping_pos.y - 50
            if self.pos.y > self.jumping_pos.y:
                self.pos.y = self.jumping_pos.y
                self.vel.y = 0
                self.acc.y = 0
                self.dec.y = 0
                self.jumping = False
                self.jumping_pos = vec(0, 0)

        # Update rect
        self.rect.midbottom = self.pos

        # Update sprites
        self.frame_count = (self.frame_count + 1) % 180  # 3 seconds
        if self.jumping:
            frame = int(self.frame_count / 90 % len(self.jump_sprites))
            self.image = self.jump_sprites[frame]
        elif self.vel.length() > 0:
            frame = int(self.frame_count / 9 % len(self.walk_sprites))
            self.image = self.walk_sprites[frame]
        else:
            frame = int(self.frame_count / 45 % len(self.stand_sprites))
            self.image = self.stand_sprites[frame]

    def blit(self):
        # Flip the image across x, y
        image = pygame.transform.flip(self.image, self.dir.x > 0, False)
        # Draw image
        self.screen.blit(image, self.rect)

import pygame

vec = pygame.math.Vector2

MAX_VELOCITY = 10.0
MAX_JUMP = 88.0


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


class Player (pygame.sprite.Sprite):
    def __init__(self, screen):

        super().__init__()

        self.screen = screen

        # Movement variables
        self.dir = vec(-1, 0)  # Start facing left, since the sprites face left
        self.pos = vec(10, 380)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.move_speed = 2.0
        self.move_gnd_friction = 0.12
        self.move_air_friction = 0.05
        self.moving = False
        self.jump_force = 3.0
        self.jump_gravity = 0.4
        self.jump_pos = vec(0, 0)
        self.jumping = False

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
        self.dir.x = -1
        self.acc.x = -self.move_speed
        self.moving = True

    def right(self):
        self.dir.x = 1
        self.acc.x = self.move_speed
        self.moving = True

    def jump(self):
        if self.jumping:
            return
        self.acc.y = -self.jump_force
        self.jump_pos = vec(self.pos.x, self.pos.y)
        self.jumping = True

    def update(self):

        # Handle physics
        if self.moving:
            ground = self.vel.x * -self.move_gnd_friction
            air = self.vel.x * -self.move_air_friction
            self.acc.x += air if self.jumping else ground
            self.vel.x = clamp(self.vel.x + self.acc.x, -
                               MAX_VELOCITY, MAX_VELOCITY)
            if self.dir.x < 0 and self.vel.x > 0:
                self.vel.x = 0
                self.acc.x = 0
                self.moving = False
            if self.dir.x > 0 and self.vel.x < 0:
                self.vel.x = 0
                self.acc.x = 0
                self.moving = False
        if self.jumping:
            self.acc.y += self.jump_gravity
            self.vel.y += self.acc.y

        # Update position
        self.pos += self.vel + 0.5 * self.acc

        # Adjust position
        if self.jumping:
            if self.pos.y < (self.jump_pos.y - MAX_JUMP):
                self.pos.y = (self.jump_pos.y - MAX_JUMP)
            if self.pos.y > self.jump_pos.y:
                self.pos.y = self.jump_pos.y
                self.vel.y = 0
                self.acc.y = 0
                self.jumping = False
                self.jumping_pos = vec(0, 0)

        # Update rect
        self.rect.midbottom = self.pos

        # Update sprites
        self.frame_count = (self.frame_count + 1) % 180  # 3 seconds
        if self.jumping:
            frame = int(self.frame_count / 90 % len(self.jump_sprites))
            self.image = self.jump_sprites[frame]
        elif self.moving:
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

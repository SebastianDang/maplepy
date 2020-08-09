import pygame
from maplepy.config import Config

vec = pygame.math.Vector2


def clamp(n, minn, maxn):
    """
    Clamps n between minn and maxn

    Args:
        n (iterable): Value to clamp
        minn (iterable): Minimum value
        maxn (iterable): Maximum value

    Returns:
        [type]: [description]
    """
    return max(min(maxn, n), minn)


class Player (pygame.sprite.Sprite):

    """
    Player class that handles physics, animation sprites, and sounds
    """

    def __init__(self):

        # pygame.sprite.Sprite
        super().__init__()

        # Movement
        self.dir = vec(0, 0)
        self.pos = vec(0, 0)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        # Config
        config = Config.instance()

        # Parameters
        self.attacking_frames = 60  # 1
        self.fall_max_speed = config['player']['fall_max_speed']
        self.jump_max_speed = config['player']['jump_max_speed']
        self.jump_force = config['player']['jump_force']
        self.jump_gravity = config['player']['jump_gravity']
        self.move_speed = config['player']['move_speed']
        self.move_max_speed = config['player']['move_max_speed']
        self.move_ground_friction = config['player']['move_ground_friction']

        # Debug parameters
        self.debug_enable = config['player']['debug']['enable']
        self.debug_rect = config['player']['debug']['rect']

        # States
        self.sprite_dir = vec(-1, 0)  # Start facing left
        self.attacking = False
        self.prone = False
        self.falling = True
        self.moving = False
        self.portal = None
        self.floor = None

        # Frame rate from screen
        self.frame_count = 0

        # Sprites
        self.sprite_prone_attack = []
        for i in range(0, 3):
            image = pygame.image.load(
                './sandbox/data/sprites/player/{}_{}.png'.format('proneStab', str(i))).convert_alpha()
            self.sprite_prone_attack.append(image)

        self.sprite_attack = []
        for i in range(0, 3):
            image = pygame.image.load(
                './sandbox/data/sprites/player/{}_{}.png'.format('stabO1', str(i))).convert_alpha()
            self.sprite_attack.append(image)

        self.sprite_prone = []
        for i in range(0, 2):
            image = pygame.image.load(
                './sandbox/data/sprites/player/{}_{}.png'.format('prone', str(i))).convert_alpha()
            self.sprite_prone.append(image)

        self.sprite_jump = []
        for i in range(0, 2):
            image = pygame.image.load(
                './sandbox/data/sprites/player/{}_{}.png'.format('jump', str(i))).convert_alpha()
            self.sprite_jump.append(image)

        self.sprite_walk = []
        for i in range(0, 4):
            image = pygame.image.load(
                './sandbox/data/sprites/player/{}_{}.png'.format('walk1', str(i))).convert_alpha()
            self.sprite_walk.append(image)

        self.sprite_stand = []
        for i in range(0, 4):
            image = pygame.image.load(
                './sandbox/data/sprites/player/{}_{}.png'.format('stand1', str(i))).convert_alpha()
            self.sprite_stand.append(image)

        # Sounds
        self.sound_attack = pygame.mixer.Sound(
            './sandbox/data/sounds/attack.wav')

        # Blit
        self.image = self.sprite_stand[0]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def on_up(self):
        pass

    def on_down(self):
        if self.prone or self.falling:
            return
        self.prone = True

    def off_down(self):
        if not self.prone:
            return
        self.prone = False

    def on_left(self):
        if self.attacking:
            return
        self.sprite_dir.x = -1
        if self.prone or self.falling:
            return
        self.dir.x = -1
        self.acc.x = -self.move_speed
        self.moving = True

    def on_right(self):
        if self.attacking:
            return
        self.sprite_dir.x = 1
        if self.prone or self.falling:
            return
        self.dir.x = 1
        self.acc.x = self.move_speed
        self.moving = True

    def off_left_or_right(self):
        if not self.moving:
            return
        self.vel.x = 0
        self.acc.x = 0
        self.moving = False

    def on_jump(self):
        if self.falling:
            return
        self.acc.y = -self.jump_force
        self.prone = False
        self.falling = True

    def off_jump(self):
        if not self.falling:
            return
        self.vel.y = 0
        self.acc.y = 0
        self.falling = False

    def on_fall(self):
        self.falling = True

    def on_attack(self):
        if self.attacking:
            return
        self.attacking = True
        self.frame_count = 0
        self.sound_attack.play()

    def place(self, x, y, fixed=False):
        if not fixed:
            self.falling = True
        self.pos.update(x, y)
        self.rect.midbottom = self.pos

    def update_image(self):

        # Frame counter
        self.frame_count = (self.frame_count + 1) % 180  # 3 seconds

        # Update animation
        if self.attacking and self.prone:
            if self.frame_count >= self.attacking_frames:
                self.attacking = False
            self.rect.midbottom = vec(self.pos.x, self.pos.y + 28)
            frame = int(self.frame_count / 20 % len(self.sprite_prone_attack))
            self.image = self.sprite_prone_attack[frame]
        elif self.attacking:
            if self.frame_count >= self.attacking_frames:
                self.attacking = False
            self.rect.midbottom = vec(self.pos.x, self.pos.y + 3)
            frame = int(self.frame_count / 20 % len(self.sprite_attack))
            self.image = self.sprite_attack[frame]
        elif self.prone:
            self.rect.midbottom = vec(self.pos.x, self.pos.y + 28)
            frame = int(self.frame_count / 90 % len(self.sprite_prone))
            self.image = self.sprite_prone[frame]
        elif self.falling:
            frame = int(self.frame_count / 90 % len(self.sprite_jump))
            self.image = self.sprite_jump[frame]
        elif self.moving:
            frame = int(self.frame_count / 7 % len(self.sprite_walk))
            self.image = self.sprite_walk[frame]
        else:
            frame = int(self.frame_count / 45 % len(self.sprite_stand))
            self.image = self.sprite_stand[frame]

        # Update rect
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.pos
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):

        # Handle physics
        if self.falling:
            self.acc.y += self.jump_gravity
            self.vel.y = clamp(self.vel.y + self.acc.y,
                               (-self.jump_max_speed), self.fall_max_speed)
        elif self.moving:
            self.acc.x += self.vel.x * -self.move_ground_friction
            self.vel.x = clamp(self.vel.x + self.acc.x,
                               (-self.move_max_speed), (self.move_max_speed))
            if (self.dir.x < 0 and self.vel.x > 0) or (self.dir.x > 0 and self.vel.x < 0):
                self.off_left_or_right()

        # Update position
        self.pos += self.vel + 0.5 * self.acc

        # Update animation
        self.update_image()

    def blit(self, surface, offset=None):

        # Draw with offset
        rect = self.rect.copy()
        if offset:
            rect = rect.move(-offset.x, -offset.y)

        # Flip the image across x, y
        image = pygame.transform.flip(self.image, self.sprite_dir.x > 0, False)

        # Draw image
        surface.blit(image, rect)

        # Draw debug
        if self.debug_enable:
            if self.debug_rect:
                pygame.draw.rect(surface, (255, 0, 0), rect, 2)

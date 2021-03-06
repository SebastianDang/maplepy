import pygame
from config import Config

vec = pygame.math.Vector2


class Background(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.image = None
        self.rect = None

    def init(self, img):
        if self.image:
            print('Already initialized.')
            return
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()

    def update(self):
        pass

    def blit(self, offset=None):

        # Draw with offset
        rect = self.rect.copy()
        if offset:
            rect = rect.move(-offset.x, -offset.y)

        # Draw image
        self.screen.blit(self.image, rect)


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.surface = None
        self.rect = None

        # Parameters
        self.platform = False
        self.player_above = False

        # Config
        config = Config.instance()

        # Debug parameters
        self.debug_enable = config['obstacle']['debug']['enable']
        self.debug_rect = config['obstacle']['debug']['rect']

    def init(self, x, y, w, h):
        if self.surface:
            print('Already initialized.')
            return
        self.surface = pygame.Surface((w, h))
        self.surface.set_alpha(0)
        self.rect = self.surface.get_rect(center=(x, y))

    def update(self):
        pass

    def blit(self, offset=None):
        if self.surface and self.rect:

            # Draw with offset
            rect = self.rect.copy()
            if offset:
                rect = rect.move(-offset.x, -offset.y)

            # Draw surface
            self.screen.blit(self.surface, rect)

            # Draw debug
            if self.debug_enable:
                if self.debug_rect:
                    # TODO: Set to 0. Some weird bug in pygame 2.0.0.dev10
                    pygame.draw.rect(self.screen, (255, 0, 0), rect, 0)


class Portal(pygame.sprite.Sprite):
    def __init__(self, screen):

        super().__init__()
        self.screen = screen

        self.surface = None
        self.rect = None

        self.pos = vec(0, 0)
        self.dest = 0

        # Config
        config = Config.instance()

        # Debug parameters
        self.debug_enable = config['portal']['debug']['enable']
        self.debug_rect = config['portal']['debug']['rect']

        # Frame rate from screen
        self.frame_count = 0

        # Sprites
        self.sprite_portal = []
        for i in range(0, 6):
            image = pygame.image.load(
                './data/sprites/portal/{}_{}.png'.format('portal', str(i))).convert_alpha()
            self.sprite_portal.append(image)

        # Blit
        self.image = self.sprite_portal[0]
        self.rect = self.image.get_rect()

    def place(self, x, y):
        self.pos.x = x
        self.pos.y = y
        self.rect.midbottom = self.pos

    def update(self):
        # Update animation
        self.frame_count = (self.frame_count + 1) % 180  # 3 seconds
        frame = int(self.frame_count / 25 % len(self.sprite_portal))
        self.image = self.sprite_portal[frame]

    def blit(self, offset=None):

        # Draw with offset
        rect = self.rect.copy()
        if offset:
            rect = rect.move(-offset.x, -offset.y)

        # Draw image
        self.screen.blit(self.image, rect)

        # Draw debug
        if self.debug_enable:
            if self.debug_rect:
                pygame.draw.rect(self.screen, (255, 0, 0), rect, 2)

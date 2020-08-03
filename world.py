import pygame
from config import Config


class Background(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen

        self.backgrounds = []
        for i in range(0, 1):
            image = pygame.image.load(
                './data/backgrounds/{}_{}.png'.format('background', str(i)))
            self.backgrounds.append(image)

        self.image = self.backgrounds[0]
        self.rect = self.image.get_rect()

    def update(self):
        pass

    def blit(self):
        self.screen.blit(self.image, self.rect)


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.surface = None
        self.rect = None

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

    def blit(self):
        if self.surface and self.rect:
            self.screen.blit(self.surface, self.rect)

            # Draw debug
            if self.debug_enable:
                if self.debug_rect:
                    pygame.draw.rect(self.screen, (255, 0, 0), self.rect, 2)

import pygame


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


class Platform(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.surface = pygame.Surface((600, 20))
        self.surface.fill((255, 0, 0))
        self.rect = self.surface.get_rect(center=(300, 390))

    def update(self):
        pass

    def blit(self):
        self.screen.blit(self.surface, self.rect)

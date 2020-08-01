import pygame


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

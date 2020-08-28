import os
import pygame


class Loading():
    """ Class that handles display for loading. """

    def __init__(self, w, h):

        # Required properties
        self.images = []
        self.images_index = 0
        self.image = None
        self.rect = pygame.Rect(0, 0, w, h)
        self.timer = 0
        self.delay = 10

    def load_images(self, path):

        # Load images
        for i in range(0, 9):
            file = '{}/ui.wz/logo.img/loading.repeat.1.{}.png'.format(
                path, str(i))
            if os.path.isfile(file):
                image = pygame.image.load(file).convert_alpha()
                image = pygame.transform.scale(image, self.rect.size)
                self.images.append(image)
            else:
                break

    def update(self):

        n = len(self.images)
        if n > 0:

            # Count timer
            self.timer += 1
            if self.timer > self.delay:

                # Reset timer
                self.timer = 0

                # Get the next image
                self.images_index = (self.images_index + 1) % n
                self.image = self.images[self.images_index]

    def blit(self, surface):

        if surface:
            if self.image:
                surface.blit(self.image, self.rect)
            else:
                surface.fill((255, 255, 255, 0))

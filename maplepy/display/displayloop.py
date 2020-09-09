import os

import pygame


class DisplayLoop():
    """ Class that handles display for looping a set of images. """

    def __init__(self, w, h):

        # Required properties
        self.images = []
        self.images_index = 0
        self.image = None
        self.rect = pygame.Rect(0, 0, w, h)
        self.timer = 0
        self.delay = 10

    def resize(self, w, h):
        """ Resizes the display """

        self.images = [pygame.transform.scale(x, (w, h)) for x in self.images]
        self.image = pygame.transform.scale(self.image, (w, h))
        self.rect = pygame.Rect(0, 0, w, h)

    def load_images(self, path, name):
        """ Load a set of images """

        self.images.clear()
        for i in range(0, 20):
            file = f'{path}/{name}.{i}.png'
            if os.path.isfile(file):
                image = pygame.image.load(file).convert_alpha()
                image = pygame.transform.scale(image, self.rect.size)
                self.images.append(image)
            else:
                break

    def update(self):
        """ Update current image to next image """

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
        """ Draw current image """

        if self.image:
            surface.blit(self.image, self.rect)
        else:
            surface.fill((255, 255, 255, 0))

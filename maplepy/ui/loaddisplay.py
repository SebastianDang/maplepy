import os
import pygame


class LoadDisplay():

    def __init__(self, w, h, path):

        # Required properties
        self.width = w
        self.height = h
        self.path = path

        self.images = []
        self.images_index = 0
        self.image = None
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.timer = 0
        self.delay = 10

        # Status
        self.loaded = False

    def load_images(self):

        # Status
        self.loaded = False

        # Load images
        for i in range(0, 9):
            file = '{}/ui.wz/logo.img/loading.repeat.1.{}.png'.format(
                self.path, str(i))
            if os.path.isfile(file):
                image = pygame.image.load(file).convert_alpha()
                self.images.append(image)
            else:
                break

        # Set image
        if self.images:
            image = self.images[0]
            self.image = pygame.transform.scale(image, self.rect.size)

        # Status
        self.loaded = True

    def update(self):

        n = len(self.images)
        if n > 0:

            self.timer += 1
            if self.timer > self.delay:

                # Reset timer
                self.timer = 0

                # Get the next image
                self.images_index = (self.images_index + 1) % n
                image = self.images[self.images_index]

                # Scale the image to the screen
                self.image = pygame.transform.scale(image, self.rect.size)

    def blit(self, surface):

        if surface:
            if self.image:
                surface.blit(self.image, self.rect)
            else:
                surface.fill((255, 255, 255, 0))

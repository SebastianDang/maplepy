import os
import pygame


class LoadDisplay():

    def __init__(self, screen, path):

        self.screen = screen
        self.path = path

        self.width = screen.get_width()
        self.height = screen.get_height()
        self.images = []
        self.images_index = 0
        self.image = None
        self.rect = None
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
            self.image = pygame.transform.scale(
                image, self.screen.get_size())
            self.rect = self.image.get_rect(
                center=(0.5 * self.width, 0.5 * self.height))

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
                self.image = pygame.transform.scale(
                    image, self.screen.get_size())

                # Center the image
                self.rect = self.image.get_rect(
                    center=(0.5 * self.width, 0.5 * self.height))

    def blit(self):

        if self.screen:
            if self.image:
                self.screen.blit(self.image, self.rect)
            else:
                self.screen.fill((255, 255, 255, 0))

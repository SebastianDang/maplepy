import logging
import os

import pygame


class SpriteDisplay():
    """
    Class that handles display and view for groups of sprites:
        Background
        Layered
        Overlay
    """

    def __init__(self, w, h):
        """
        Contains a separate background surface to draw explicit background images
        Contains background and layered sprites that have to be loaded with some data
        """

        # Required properties
        self.width = w
        self.height = h

        # User view
        self.view = pygame.Rect(0, 0, w, h)
        self.view_limit = None

        # Background
        self.background = pygame.Surface((w, h))
        self.background_fixed = False
        self.background_sprites = None

        # Objects in the map
        self.layered_sprites = []

        # Items are always on top
        self.overlayed_sprites = None

    def resize(self, w, h):
        """ Resizes the display """

        # Update properties
        self.width = w
        self.height = h

        # Update view
        x = self.view.x if self.view else 0
        y = self.view.y if self.view else 0
        self.view = pygame.Rect(x, y, w, h)

        # Update background surface
        if not self.background_fixed:
            self.background = pygame.Surface((w, h))

    def move_view(self, x, y):
        """ Moves the view rect """
        self.view = self.view.move(x, y)

    def set_view_limit(self, x, y, width, height):
        """ Updates the view limit rect """
        self.view_limit = pygame.Rect(x, y, width, height)

    def set_fixed_background(self, width, height):
        """ Sets the background to fixed size """
        self.background = pygame.Surface((width, height))
        self.background_fixed = True

    def update(self):
        """
        Update camera and sprites
        Camera:
            If view is larger than view_limit,
            view is centered inside of view_limit,
            but its size is unchanged.
        """

        # Camera
        if self.view and self.view_limit:
            self.view = self.view.clamp(self.view_limit)

        # Background
        if self.background_sprites:
            self.background_sprites.update()

        # Tiles / Objs / Others
        for sprites in self.layered_sprites:
            sprites.update()

        # UI
        if self.overlayed_sprites:
            self.overlayed_sprites.update()

    def blit(self, surface):
        """
        Draw background sprites onto a separate surface, then scale it to the target surface
        Draw layered sprites together, ordered by layer index
        Draw overlayed sprites last, always on top
        """

        # Background
        if self.background and self.background_sprites:

            # Blit onto background surface
            self.background.fill((0, 0, 0))
            self.background_sprites.blit(self.background, self.view)

            # Scale background surface and blit to target surface
            background = pygame.transform.smoothscale(self.background, surface.get_size())
            surface.blit(background, surface.get_rect())

        # Tiles / Objs / Others
        for sprites in self.layered_sprites:
            sprites.blit(surface, self.view)

        # UI
        if self.overlayed_sprites:
            self.overlayed_sprites.blit(surface)


class ImageDisplay():
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

    def load(self, path, name):
        """ Load a set of images: {path}/{name}.{count}.png """

        self.images.clear()
        for i in range(20):
            file = f'{path}/{name}.{i}.png'
            if os.path.isfile(file):
                image = pygame.image.load(file).convert_alpha()
                image = pygame.transform.scale(image, self.rect.size)
                self.images.append(image)
            else:
                logging.warning(f'{file} does not exist')
                break

    def update(self):
        """ Update current image to next image """

        # Update if there is more than one image
        n = len(self.images)
        if n > 1:

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

import pygame


class Display():
    """
    Class that handles display and view for groups of sprites:
        Background
        Layered
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
        self.background_sprites = None

        # Objects in the map
        self.layered_sprites = []

        # Items are alwauys on top
        self.overlayed_sprites = None

    def resize(self, w, h):
        """ Resizes the display """
        self.width = w
        self.height = h
        x = self.view.x if self.view else 0
        y = self.view.y if self.view else 0
        self.view = pygame.Rect(x, y, w, h)
        self.background = pygame.Surface((w, h))

    def move_view(self, x, y):
        """ Moves the view rect """
        self.view = self.view.move(x, y)

    def set_view_limit(self, x, y, width, height):
        """ Updates the view limit rect """
        self.view_limit = pygame.Rect(x, y, width, height)

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
            background = pygame.transform.scale(
                self.background, surface.get_size())
            surface.blit(background, surface.get_rect())

        # Tiles / Objs / Others
        for sprites in self.layered_sprites:
            sprites.blit(surface, self.view)

        # UI
        if self.overlayed_sprites:
            self.overlayed_sprites.blit(surface)

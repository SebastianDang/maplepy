import math
import pygame


class BackgroundSprites():
    """ Class that draws background sprites """

    def __init__(self):
        """ Contains a layered sprite group. This has to be loaded with some data """
        self.sprites = pygame.sprite.LayeredUpdates()

    def calculate_cam_offset(self, rx, dx, z):
        """ Calculate the camera x or y offset """
        return float(rx * (dx + z) / 100) + z

    def calculate_tile_offset(self, w, x, cx):
        """ Calculate the tile starting x or y offset """
        return math.ceil((-w - x) / cx) * cx

    def update(self):
        """ Update all sprites """
        for sprite in self.sprites:
            try:
                sprite.update()
            except:
                continue

    def blit(self, surface, offset=None):
        """ Draw all sprites """

        # Get surface properties
        w, h = surface.get_size()

        # For all sprites
        for sprite in self.sprites:
            try:

                # Get rect with animation offset
                rect = sprite.rect.move(sprite.dx, sprite.dy)

                # Camera offset
                dx = offset.x if offset else 0
                dy = offset.y if offset else 0
                x = self.calculate_cam_offset(sprite.rx, dx, 0.5 * w)
                y = self.calculate_cam_offset(sprite.ry, dy, 0.5 * h)
                rect = rect.move(x, y)

                # 0 - Simple image (eg. the hill with the tree in the background of Henesys)
                if sprite.type == 0:
                    surface.blit(sprite.image, rect)

                # 1 - Image is copied horizontally (eg. the sea in Lith Harbor)
                # 2 - Image is copied vertically (eg. trees in maps near Ellinia)
                # 3 - Image is copied in both directions (eg. the background sky color square in many maps)
                # 4 - Image scrolls and is copied horizontally (eg. clouds)
                # 5 - Image scrolls and is copied vertically (eg. background in the Helios Tower elevator)
                # 6 - Image scrolls horizontally, and is copied in both directions (eg. the train in Kerning City subway JQ)
                # 7 - Image scrolls vertically, and is copied in both directions (eg. rain drops in Ellin PQ maps)
                horizontal = [1, 4]
                if sprite.type in horizontal and sprite.cx > 0:
                    dx = self.calculate_tile_offset(
                        sprite.rect.width, rect.x, sprite.cx)
                    htile = rect.move(dx, 0)
                    while htile.x < w:
                        surface.blit(sprite.image, htile)
                        htile = htile.move(sprite.cx, 0)
                vertical = [2, 5]
                if sprite.type in vertical and sprite.cy > 0:
                    dy = self.calculate_tile_offset(
                        sprite.rect.height, rect.y, sprite.cy)
                    vtile = rect.move(0, dy)
                    while vtile.y < h:
                        surface.blit(sprite.image, vtile)
                        vtile = vtile.move(0, sprite.cy)
                both = [3, 6, 7]
                if sprite.type in both and sprite.cx > 0 and sprite.cy > 0:
                    dx = self.calculate_tile_offset(
                        sprite.rect.width, rect.x, sprite.cx)
                    dy = self.calculate_tile_offset(
                        sprite.rect.height, rect.y, sprite.cy)
                    vtile = rect.move(dx, dy)
                    while vtile.y < h:
                        htile = vtile.copy()
                        while htile.x < w:
                            surface.blit(sprite.image, htile)
                            htile = htile.move(sprite.cx, 0)
                        vtile = vtile.move(0, sprite.cy)

            except:
                continue


class LayeredSprites():
    """ Class that draws layered sprites """

    def __init__(self):
        """ Contains a layered sprite group. This has to be loaded with some data """
        self.sprites = pygame.sprite.LayeredUpdates()

    def update(self):
        """ Update all sprites """
        for sprite in self.sprites:
            try:
                sprite.update()
            except:
                continue

    def blit(self, surface, offset=None):
        """ Draw all sprites """

        # For all sprites
        for sprite in self.sprites:
            try:

                # Get rect
                rect = sprite.rect

                # Camera offset
                if offset:

                    # If the sprite is outside the surface
                    if not sprite.rect.colliderect(offset):
                        continue

                    rect = sprite.rect.move(-offset.x, -offset.y)

                # Draw
                surface.blit(sprite.image, rect)

            except:
                continue

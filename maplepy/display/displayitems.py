import pygame


class BackgroundSprites():
    """ Class that draws background sprites """

    def __init__(self):
        """ Contains a sprite group. This has to be loaded with some data """
        self.sprites = pygame.sprite.LayeredUpdates()

    def calculate_x(self, rx, dx, z):
        """ Calculate the camera x offset """
        return float(rx * (dx + z) / 100) + z

    def calculate_y(self, ry, dy, z):
        """ Calculate the camera y offset """
        return float(ry * (dy + z) / 100) + z

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
                x = self.calculate_x(sprite.rx, dx, 0.5 * w)
                y = self.calculate_y(sprite.ry, dy, 0.5 * h)
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
                horizontal = [1, 3, 4, 6, 7]
                if sprite.type in horizontal:
                    if sprite.cx > 0:
                        tile = rect.copy()
                        while tile.x < w:
                            surface.blit(sprite.image, tile)
                            tile = tile.move(sprite.cx, 0)
                        tile = rect.copy()
                        while tile.x > -sprite.rect.width:
                            surface.blit(sprite.image, tile)
                            tile = tile.move(-sprite.cx, 0)
                vertical = [2, 3, 5, 6, 7]
                if sprite.type in vertical:
                    if sprite.cy > 0:
                        tile = rect.copy()
                        while tile.y < h:
                            surface.blit(sprite.image, tile)
                            tile = tile.move(0, sprite.cy)
                        tile = rect.copy()
                        while tile.y > -sprite.rect.height:
                            surface.blit(sprite.image, tile)
                            tile = tile.move(0, -sprite.cy)

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

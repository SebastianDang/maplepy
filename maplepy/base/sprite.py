import logging
import math

import pygame


class BackgroundSprites():
    """ Class that draws from a list of background sprites """

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
                logging.exception('Failed to update background')
                continue

    def blit(self, surface, offset=None):
        """ Draw all sprites """

        # Get surface properties
        w, h = surface.get_size()
        cx = offset.centerx - surface.get_rect().centerx if offset else 0
        cy = offset.centery - surface.get_rect().centery if offset else 0

        # For all sprites
        for sprite in self.sprites:
            try:

                # Get rect with animation offset
                rect = sprite.rect.move(sprite.dx, sprite.dy)

                # Camera offset
                x = self.calculate_cam_offset(sprite.rx, cx, 0.5 * w)
                y = self.calculate_cam_offset(sprite.ry, cy, 0.5 * h)
                rect = rect.move(x, y)

                # 0 - Simple image (eg. the hill with the tree in the background of Henesys)
                if sprite.type == 0:
                    surface.blit(sprite.image, rect)

                # 1 - Image is copied horizontally (eg. the sea in Lith Harbor)
                # 4 - Image scrolls and is copied horizontally (eg. clouds)
                horizontal = [1, 4]
                if sprite.type in horizontal and sprite.cx > 0:
                    dx = self.calculate_tile_offset(
                        sprite.rect.width, rect.x, sprite.cx)
                    htile = rect.move(dx, 0)
                    while htile.x < w:
                        surface.blit(sprite.image, htile)
                        htile = htile.move(sprite.cx, 0)

                # 2 - Image is copied vertically (eg. trees in maps near Ellinia)
                # 5 - Image scrolls and is copied vertically (eg. background in the Helios Tower elevator)
                vertical = [2, 5]
                if sprite.type in vertical and sprite.cy > 0:
                    dy = self.calculate_tile_offset(
                        sprite.rect.height, rect.y, sprite.cy)
                    vtile = rect.move(0, dy)
                    while vtile.y < h:
                        surface.blit(sprite.image, vtile)
                        vtile = vtile.move(0, sprite.cy)

                # 3 - Image is copied in both directions (eg. the background sky color square in many maps)
                # 6 - Image scrolls horizontally, and is copied in both directions (eg. the train in Kerning City subway JQ)
                # 7 - Image scrolls vertically, and is copied in both directions (eg. rain drops in Ellin PQ maps)
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
                logging.exception('Failed to blit background')
                continue


class LayeredSprites():
    """ Class that draws from a list of layered sprites """

    def __init__(self):
        """ Contains a layered sprite group. This has to be loaded with some data """

        self.sprites = pygame.sprite.LayeredUpdates()

    def update(self):
        """ Update all sprites """

        for sprite in self.sprites:
            try:
                sprite.update()
            except:
                logging.exception('Failed to update layer')
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
                logging.exception('Failed to blit layer')
                continue


class ConsoleSprite(pygame.sprite.Sprite):
    """ Class that handles display for text that belongs within a 'console'. """

    def __init__(self, w, h):

        # pygame.sprite.Sprite
        super().__init__()
        self.image = pygame.surface.Surface((w, h))
        self.image.fill((20, 20, 20))
        self.image.set_alpha(100)  # transparent
        self.rect = self.image.get_rect()

        # pygame.font.Font
        self.font = pygame.font.Font(None, 24)

    def draw_wrapped(self, surface, text, color, rect, font, aa=True):

        # Starting params
        line_y = rect.top
        line_space = -2
        font_height = font.size('Tg')[1]

        while text:

            # Starting index
            i = 1

            # Check if the current row will be outside rect
            if line_y + font_height > rect.bottom:
                break

            # Determine maximum width of line
            while i < len(text) and font.size(text[:i])[0] < rect.width:
                i += 1

            # Edge case
            if font.size(text[:i])[0] > rect.width:
                i -= 1

            # Adjust the wrap to the last word, if theres a space
            if i < len(text):
                space = text.rfind(' ', 0, i) + 1
                i = space if space > 0 else i

            # Render the line and blit it to the surface
            image = font.render(text[:i], aa, color)
            surface.blit(image, (rect.left, line_y))

            # Move to the next line
            line_y += font_height + line_space

            # Remove the text we just blitted
            text = text[i:]

        # Return any remaining text
        return text

    def update(self):
        pass

    def blit(self, surface, text):

        # Blit the background
        surface.blit(self.image, self.rect)

        # Blit text
        self.draw_wrapped(surface, text, (255, 255, 255), self.rect, self.font)


class DataSprite(pygame.sprite.Sprite):
    """ Helper class to load byte array images as pygame sprites """

    def __init__(self):

        # pygame.sprite.Sprite
        super().__init__()
        self.image = None
        self.rect = None
        self.mask = None

        # byte data
        self.width = 0
        self.height = 0
        self.data = []

    def load(self, w, h, data):
        """
        Load image from byte array

        Each pixel is 4 bytes (32-bit) represented by:

            b   g   r   a

        Pygame stores image data as 4 bytes (32-bit) represented by:

            r   g   b   a

        Args:
            w (int): target image width
            h (int): target image height
            data (array[int]): byte array
        """

        try:

            if True:  # Automatic buffer method

                # Swap b and r (b,r = r,b)
                # data[0::4], data[2::4] = data[2::4], data[0::4]

                # Create a new image
                image = pygame.image.frombuffer(data, (w, h), 'RGBA')

            else:  # Manually loop

                # Create a new image
                image = pygame.Surface((w, h), pygame.SRCALPHA)
                # image.set_colorkey((0, 0, 0, 0))  # Transparent

                # Create pixel array to access x,y coordinates
                pxarray = pygame.PixelArray(image)
                for y in range(0, h):
                    for x in range(0, w):
                        b = data[(y*w*4) + (x*4) + 0]
                        g = data[(y*w*4) + (x*4) + 1]
                        r = data[(y*w*4) + (x*4) + 2]
                        a = data[(y*w*4) + (x*4) + 3]
                        pxarray[x, y] = (r, g, b, a)

                # pixel array must be deleted to 'unlock' the image
                del pxarray

                # Call unlock, to be safe
                image.unlock()

            # Update current sprite
            self.image = image.convert_alpha()
            self.rect = image.get_rect()
            self.mask = pygame.mask.from_surface(image)
            self.width = w
            self.height = h
            self.data = data

        except:
            logging.exception('Failed to load image')

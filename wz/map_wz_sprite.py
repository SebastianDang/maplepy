import os
import sys
import pygame
from map_wz import *
vec = pygame.math.Vector2


class map_wz_sprite(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.map_wz = None
        self.images = {}

    def load_wz(self, xml):
        self.map_wz = map_wz()
        self.map_wz.open(xml)
        self.map_wz.parse_root()

    def load_bg_images(self):
        if not self.map_wz:
            return

        # Get unique backgrounds
        name = []
        for bg in self.map_wz.bg:
            name.append(bg['bS'])
        name = set(name)

        # Load backgrounds
        for n in name:
            images = []
            for i in range(0, 100):  # Max num of images
                path = './img/{}/{}.{}.png'.format(n, 'back', str(i))
                if os.path.isfile(path):
                    image = pygame.image.load(path).convert_alpha()
                    images.append(image)
                else:
                    break
            self.images[n] = images

    def draw_bg(self, offset):

        # Get surface properties
        w, h = pygame.display.get_surface().get_size()

        # Render background
        for bg in self.map_wz.bg:
            try:
                name = bg['name']
                bS = bg['bS']
                no = int(bg['no'])
                x = int(bg['x'])
                y = int(bg['y'])
                t = int(bg['type'])

                # Get image
                images = self.images[bS]
                image = images[no]

                # Image offset
                rect = image.get_rect().copy().move(x, y)

                # Camera offset
                if offset:
                    rect = rect.move(-offset.x, -offset.y)

                # 0 - Simple image (eg. the hill with the tree in the background of Henesys)
                # 1 - Image is copied horizontally (eg. the sea in Lith Harbor)
                # 2 - Image is copied vertically (eg. trees in maps near Ellinia)
                # 3 - Image is copied in both directions (eg. the background sky color square in many maps)
                # 4 - Image scrolls and is copied horizontally (eg. clouds)
                # 5 - Image scrolls and is copied vertically (eg. background in the Helios Tower elevator)
                # 6 - Image scrolls horizontally, and is copied in both directions (eg. the train in Kerning City subway JQ)
                # 7 - Image scrolls vertically, and is copied in both directions (eg. rain drops in Ellin PQ maps)
                # TODO: Handle velocities
                horizontal = [1, 3, 4, 6, 7]
                vertical = [2, 3, 5, 6, 7]

                # Type
                if t == 0:  # Static image
                    self.screen.blit(image, rect)
                elif t in horizontal:  # Copied horizontally
                    tile = rect.copy()
                    while tile.x > -tile.width:  # TODO: Don't do this the lazy way
                        self.screen.blit(image, tile)
                        tile = tile.move(-tile.width, 0)
                    tile = rect.copy()
                    while tile.x < w:
                        self.screen.blit(image, tile)
                        tile = tile.move(tile.width, 0)
                elif t in vertical:  # Copied vertically
                    tile = rect.copy()
                    while tile.y > -tile.height:  # TODO: Don't do this the lazy way
                        self.screen.blit(image, tile)
                        tile = tile.move(0, -tile.height)
                    tile = rect.copy()
                    while tile.y < h:
                        self.screen.blit(image, tile)
                        tile = tile.move(0, tile.height)

            except:
                continue

    def update(self):
        pass

    def blit(self, offset=None):

        self.draw_bg(offset)


if __name__ == "__main__":
    print(map_wz_sprite.__name__)
    pygame.init()
    w, h = 1920, 1200
    screen = pygame.display.set_mode((w, h))
    cam = pygame.Rect(0, 0, w, h)
    m = map_wz_sprite(screen)
    m.load_wz('./xml/100000000.xml')  # Henesys
    m.load_bg_images()
    while(True):
        # Events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.event.clear()
                pygame.quit()
                sys.exit()
        pygame.event.pump()
        # Camera movement test
        speed = 10
        inputs = pygame.key.get_pressed()
        if inputs[pygame.K_UP]:
            cam = cam.move(0, -speed)
        if inputs[pygame.K_DOWN]:
            cam = cam.move(0, speed)
        if inputs[pygame.K_LEFT]:
            cam = cam.move(-speed, 0)
        if inputs[pygame.K_RIGHT]:
            cam = cam.move(speed, 0)
        if inputs[pygame.K_r]:
            cam.x = 0
            cam.y = 0
        # Draw
        screen.fill((0, 0, 0))
        m.blit(cam)
        pygame.display.update()

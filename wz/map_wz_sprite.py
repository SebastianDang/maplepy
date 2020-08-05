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
                path = './Back/{}/{}.{}.png'.format(n, 'back', str(i))
                if os.path.isfile(path):
                    image = pygame.image.load(path).convert_alpha()
                    images.append(image)
                else:
                    break
            self.images[n] = images

    def load_tile_images(self):
        if not self.map_wz:
            return

        # Get unique tiles
        name = []
        for tile in self.map_wz.all_tiles:
            if 'tS' in tile['info']:
                name.append(tile['info']['tS'])
        name = set(name)

        # Load tiles
        image_set = {}
        types = ['bsc', 'edD', 'edU', 'enH0', 'enH1',
                 'enV0', 'enV1', 'slLD', 'slLU', 'slRD', 'slRU']
        for n in name:
            for t in types:
                images = []
                for i in range(0, 100):  # Max num of images
                    path = './data/Tile/{}/{}.{}.png'.format(n, t, str(i))
                    if os.path.isfile(path):
                        image = pygame.image.load(path).convert_alpha()
                        images.append(image)
                    else:
                        break
                image_set[t] = images
            self.images[n] = image_set

    def load_object_images(self):
        if not self.map_wz:
            return

        # Get unique objects
        oS_set = []
        l0_set = []
        l1_set = []
        l2_set = []
        for obj in self.map_wz.all_objects:
            oS_set.append(obj['oS'])
            l0_set.append(obj['l0'])
            l1_set.append(obj['l1'])
            l2_set.append(obj['l2'])
        oS_set = set(oS_set)
        l0_set = set(l0_set)
        l1_set = set(l1_set)
        l2_set = set(l2_set)

        # Load objects
        for oS in oS_set:
            subimages = {}
            for l0 in l0_set:
                for l1 in l1_set:
                    for l2 in l2_set:
                        images = []
                        for i in range(0, 10):
                            path = './data/Obj/{}/{}.{}.{}.{}.png'.format(
                                oS, l0, l1, l2, str(i))
                            if os.path.isfile(path):
                                image = pygame.image.load(path).convert_alpha()
                                images.append(image)
                            else:
                                break
                        subimages["{}.{}.{}".format(l0, l1, l2)] = images
            self.images[oS] = subimages

    def draw_bg(self, offset=None):

        # Get surface properties
        w, h = pygame.display.get_surface().get_size()

        # Draw background
        for bg in self.map_wz.bg:
            try:
                name = bg['name']
                bS = bg['bS']
                no = int(bg['no'])
                x = int(bg['x'])
                y = int(bg['y'])
                f = int(bg['f'])
                t = int(bg['type'])

                # Get image
                images = self.images[bS]
                image = images[no]
                rect = image.get_rect().copy()

                # Image offset
                rect.topleft = vec(x, y)

                # Image flip
                if f > 0:
                    image = pygame.transform.flip(image, True, False)

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

    def draw_tiles(self, offset=None):

        # Draw tiles
        for tile in self.map_wz.all_tiles:
            try:
                tS = tile['info']['tS']
                tSMag = tile['info']['tSMag'] if 'tSMag' in tile['info'] else None
                forbidFallDown = tile['info']['forbidFallDown'] if 'forbidFallDown' in tile['info'] else None
                x = int(tile['x'])
                y = int(tile['y'])
                u = tile['u']
                no = int(tile['no'])
                zM = int(tile['zM'])

                # Get image
                images = self.images[tS][u]
                image = images[no]
                rect = image.get_rect().copy()

                # Image offset
                rect.bottomleft = vec(x, y)

                # Camera offset
                if offset:
                    rect = rect.move(-offset.x, -offset.y)

                # Draw
                self.screen.blit(image, rect)

            except:
                continue

    def draw_objects(self, offset=None):

        # Draw tiles
        for obj in self.map_wz.all_objects:
            try:
                x = int(obj['x'])
                y = int(obj['y'])
                f = int(obj['f'])
                oS = obj['oS']
                l0 = obj['l0']
                l1 = obj['l1']
                l2 = obj['l2']

                # Get image
                images = self.images[oS]["{}.{}.{}".format(l0, l1, l2)]
                image = images[0]
                rect = image.get_rect().copy()

                # Image offset
                rect.center = vec(x, y)

                # Image flip
                if f > 0:
                    image = pygame.transform.flip(image, True, False)

                # Camera offset
                if offset:
                    rect = rect.move(-offset.x, -offset.y)

                # Draw
                self.screen.blit(image, rect)

            except:
                continue

    def update(self):
        pass

    def blit(self, offset=None):

        self.draw_bg(offset)
        self.draw_tiles(offset)
        self.draw_objects(offset)


if __name__ == "__main__":
    print(map_wz_sprite.__name__)
    pygame.init()
    w, h = 1920, 1200
    screen = pygame.display.set_mode((w, h))
    cam = pygame.Rect(0, 0, w, h)
    m = map_wz_sprite(screen)
    m.load_wz('./xml/000010000.xml')
    m.load_bg_images()
    m.load_tile_images()
    m.load_object_images()
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

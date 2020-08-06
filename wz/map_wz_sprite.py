import os
import sys
import pygame
from map_wz import *
from Tile_sprites import Tile_sprites
from Tile_xml import Tile_xml
from Tile_obj import Tile_obj
from Object_sprites import Object_sprites
from Object_xml import Object_xml
from Object_obj import Object_obj
vec = pygame.math.Vector2


class map_wz_sprite(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.map_wz = None
        self.images = {}
        self.tile_sprites_list = []
        self.object_sprites_list = []

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
                path = './data/Back/{}/{}.{}.png'.format(n, 'back', str(i))
                if os.path.isfile(path):
                    image = pygame.image.load(path).convert_alpha()
                    images.append(image)
                else:
                    break
            self.images[n] = images

    def load_tile_sprites(self):
        if not self.map_wz:
            return

        for tile_instances in self.map_wz.all_tiles:
            info = tile_instances['info']
            if 'tS' in info:
                # Get tile name
                tile_name = info['tS']
                # Create sprites
                tile_sprites = Tile_sprites(self.screen)
                tile_sprites.load_xml(
                    "{}/data/Tile/{}.img.xml".format('.', tile_name))
                tile_sprites.load_sprites("{}".format('.'))
                tile_sprites.load_tiles(tile_instances['tiles'])
            self.tile_sprites_list.append(tile_sprites)

    def load_object_sprites(self):
        if not self.map_wz:
            return
        for object_instances in self.map_wz.all_objects:
            info = object_instances['info']
            # TODO: Check if really unique, we only want to do this once
            oS_set = []
            for obj in object_instances['objects']:
                oS_set.append(obj['oS'])
            oS_set = set(oS_set)
            for oS in oS_set:
                # Create sprites
                object_sprites = Object_sprites(self.screen)
                object_sprites.load_xml(
                    "{}/data/Obj/{}.img.xml".format('.', oS))
                object_sprites.load_sprites("{}".format('.'))
                object_sprites.load_objects(object_instances['objects'])
                self.object_sprites_list.append(object_sprites)

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
        for tile_sprites in self.tile_sprites_list:
            tile_sprites.blit(offset)

    def draw_objects(self, offset=None):
        for object_sprites in self.object_sprites_list:
            object_sprites.blit(offset)

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
    # m.load_wz('./xml/100000000.xml')
    m.load_bg_images()
    m.load_tile_sprites()
    m.load_object_sprites()
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

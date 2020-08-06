import os
import pygame

from Tile_xml import Tile_xml
from Tile_obj import Tile_obj


vec = pygame.math.Vector2


class Tile_sprites(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.xml = None
        self.sprites = None
        self.tiles = None

    def load_xml(self, xml):
        self.xml = Tile_xml()
        self.xml.open(xml)
        self.xml.parse_root()

    def load_sprites(self, path):
        if not self.xml:
            return
        sprites = {}
        for tile in self.xml.tiles:
            images = []
            for index in range(0, 20):  # Max num of frames
                file = "{}/data/Tile/{}/{}.{}.png".format(
                    path, self.xml.name, tile, str(index))
                if os.path.isfile(file):
                    image = pygame.image.load(file).convert_alpha()
                    images.append(image)
                else:
                    break
            sprites[tile] = images
        self.sprites = sprites

    def load_tiles(self, tile_instances):
        tiles = []
        for instance in tile_instances:
            try:
                # Instance properties
                x = int(instance['x'])
                y = int(instance['y'])
                u = instance['u']
                no = int(instance['no'])
                zM = int(instance['zM'])
                # Tile properties
                tile_data = self.xml.tiles[u][no]
                cx = int(tile_data['cx'])
                cy = int(tile_data['cy'])
                z = int(tile_data['z'])
                # Tile sprite
                sprites = self.sprites[u]
                sprite = sprites[no]
                # Build tile object
                tile = Tile_obj()
                tile.x = x
                tile.y = y
                tile.z = z
                tile.cx = cx
                tile.cy = cy
                tile.u = u
                tile.no = no
                tile.zM = zM
                tile.sprite = sprite
                # Explicit special case
                if tile.z:
                    tile.zM = tile.z
                # Add to list
                tiles.append(tile)

            except:
                print('Error while loading tiles')
                continue
        # Pre process and sort by z
        tiles = sorted(tiles, key=lambda k: k.zM)
        self.tiles = tiles

    def update(self):
        pass

    def blit(self, offset=None):

        for tile in self.tiles:
            try:
                # Get image
                image = tile.sprite
                rect = image.get_rect().copy()

                # Check offset
                if offset and not rect.colliderect(offset):
                    continue

                # Image offset
                rect.topleft = (-tile.cx, -tile.cy)
                rect = rect.move(tile.x, tile.y)

                # Camera offset
                if offset:
                    rect = rect.move(-offset.x, -offset.y)

                # Draw
                self.screen.blit(image, rect)
            except:
                continue

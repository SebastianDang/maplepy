import os
import pygame

from Tile.Tile_xml import Tile_xml
from Tile.Tile_obj import Tile_obj


vec = pygame.math.Vector2


class Tile_sprites(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.xml = None
        self.sprites = None
        self.objects = None

    def load_xml(self, name, path):

        # Check if xml has already been loaded before
        if self.xml:
            print('Xml was already loaded.')
            return

        # Load and parse the xml
        file = "{}/Tile/{}.img.xml".format(path, name)
        self.xml = Tile_xml()
        self.xml.open(file)
        self.xml.parse_root()

    def load_sprites(self, path):

        # Check if xml has finished loading
        if not self.xml or not self.xml.objects:
            print('Xml was not loaded yet.')
            return

        # Load sprites for a given xml file
        sprites = {}
        for obj in self.xml.objects:
            images = []
            for index in range(0, 20):  # Max num of frames
                file = "{}/Tile/{}/{}.{}.png".format(
                    path, self.xml.name, obj, str(index))
                if os.path.isfile(file):
                    image = pygame.image.load(file).convert_alpha()
                    images.append(image)
                else:
                    break
            sprites[obj] = images

        # Set images
        self.sprites = sprites

    def clear_objects(self):
        self.objects.clear()

    def load_objects(self, object_instances):

        # Check if xml has finished loading
        if not self.xml or not self.xml.objects:
            return

        # Go through instances list and add
        objects = []
        for instance in object_instances:
            try:

                # Build object
                obj = Tile_obj()

                # Required properties
                obj.x = int(instance['x'])
                obj.y = int(instance['y'])
                obj.u = instance['u']
                obj.no = int(instance['no'])
                obj.zM = int(instance['zM'])

                # Get sprite by key and index
                sprites = self.sprites[obj.u]
                sprite = sprites[obj.no]
                obj.sprite = sprite

                # Get additional properties
                obj_data = self.xml.objects[obj.u][obj.no]
                obj.center_x = int(obj_data['x'])
                obj.center_y = int(obj_data['y'])
                obj.z = int(obj_data['z'])

                # Explicit special case
                if obj.z:
                    obj.zM = obj.z

                # Add to list
                objects.append(obj)

            except:
                print('Error while loading tiles')
                continue

        # Pre process and sort by z
        objects = sorted(objects, key=lambda k: k.zM)
        self.objects = objects

    def update(self):
        pass

    def blit(self, offset=None):
        if not self.objects:
            return
        for obj in self.objects:
            try:
                # Get image
                image = obj.sprite
                rect = image.get_rect().copy()

                # Image offset
                rect.topleft = (-obj.center_x, -obj.center_y)
                rect = rect.move(obj.x, obj.y)

                # Check offset
                if offset and not rect.colliderect(offset):
                    continue

                # Camera offset
                if offset:
                    rect = rect.move(-offset.x, -offset.y)

                # Draw
                self.screen.blit(image, rect)
            except:
                print('Error while drawing tiles')
                continue

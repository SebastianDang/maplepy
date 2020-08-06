import os
import pygame

from Back_xml import Back_xml
from Back_obj import Back_obj


vec = pygame.math.Vector2


class Back_sprites(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.xml = {}
        self.sprites = {}
        self.objects = []

    def load_xml(self, name, path):

        # Check if xml has already been loaded before
        if name in self.xml:
            print('{} was already loaded.'.format(name))
            return

        # Load and parse the xml
        file = "{}/Back/{}.img.xml".format(path, name)
        self.xml[name] = Back_xml()
        self.xml[name].open(file)
        self.xml[name].parse_root()

    def load_sprites(self, name, path):

        # Check if xml has finished loading
        if name not in self.xml or not self.xml[name].objects:
            print('{} was not loaded yet.'.format(name))
            return

        # Get current xml file
        xml = self.xml[name]

        # Load sprites for a given xml file
        sprites = []
        for index in range(0, 100):  # Num images
            file = "{}/Back/{}/back.{}.png".format(
                path, name, str(index))
            if os.path.isfile(file):
                image = pygame.image.load(file).convert_alpha()
                sprites.append(image)
            else:
                break

        # Set images
        self.sprites[name] = sprites

    def clear_objects(self):
        self.objects.clear()

    def load_objects(self, name, object_instances):

        # Check if xml has finished loading
        if name not in self.xml or not self.xml[name].objects:
            print('{} was not loaded yet.'.format(name))
            return

        # Go through instances list and add
        objects = []
        for instance in object_instances:
            try:

                # Build object
                obj = Back_obj()

                # Required properties
                obj.bS = instance['bS']
                obj.x = int(instance['x'])
                obj.y = int(instance['y'])
                obj.cx = int(instance['cx'])
                obj.cy = int(instance['cy'])
                obj.rx = int(instance['rx'])
                obj.ry = int(instance['ry'])
                obj.f = int(instance['f'])
                obj.no = int(instance['no'])
                obj.a = int(instance['a'])
                obj.type = int(instance['type'])
                obj.front = int(instance['front'])
                obj.ani = int(instance['ani'])

                # Get sprite by key and index
                sprites = self.sprites[obj.bS]
                sprite = sprites[obj.no]
                obj.sprite = sprite

                # Get additional properties
                try:
                    obj.z = 0
                    obj.width = 0
                    obj.height = 0

                    # Extract data
                    object_data = self.xml[name].objects
                    back_data = object_data['back']

                    # Set data
                    data = back_data[obj.no]
                    obj.z = int(data['z'])
                    obj.width = int(data['width'])
                    obj.height = int(data['height'])

                    # Explicit special case
                    if obj.cx == 0:
                        obj.cx = int(instance['cx'])
                    if obj.cy == 0:
                        obj.cy = int(instance['cy'])

                except:
                    pass

                # Add to list
                objects.append(obj)

            except:
                print('Error while loading back')
                continue

        self.objects = objects

    def calculate_back_x(self, dx, rx, z):
        return (rx * (dx + z) / 100)

    def calculate_back_y(self, dy, ry, z):
        return (ry * (dy + z) / 100)

    def update(self):
        horizontal = [4, 6]
        vertical = [5, 7]
        for obj in self.objects:
            if obj.width > 0:
                obj.frame_count = (obj.frame_count + 1) % obj.width

    def blit(self, offset=None):
        if not self.objects:
            return

        # Get surface properties
        w, h = pygame.display.get_surface().get_size()

        # For all objects
        for obj in self.objects:
            try:
                # Get image
                image = obj.sprite
                rect = image.get_rect().copy()

                # Image offset
                rect.center = (-obj.cx, -obj.cy)
                rect = rect.move(obj.x, obj.y)

                # Image flip
                if obj.f > 0:
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

                if obj.type == 0:
                    self.screen.blit(image, rect)
                elif obj.type == 1:
                    delta = obj.cx if obj.cx > 0 else rect.width
                    tile = rect.copy()
                    while tile.x < w:
                        self.screen.blit(image, tile)
                        tile = tile.move(delta, 0)
                    tile = rect.copy()
                    while tile.x > -tile.width:
                        self.screen.blit(image, tile)
                        tile = tile.move(-delta, 0)
                elif obj.type == 2:
                    pass
                elif obj.type == 3:
                    pass
                elif obj.type == 4:

                    # # Tile rect
                    # tile = rect.copy()

                    # # Scroll horizontally
                    # if obj.rx != 0:
                    #     delta = obj.frame_count / obj.rx
                    #     tile = tile.move(int(delta), 0)

                    # # Copy horizontally
                    # if tile.right > 0:
                    #     delta = tile.width * (tile.right % tile.width)
                    #     tile = tile.move(-delta, 0)
                    # while tile.x < w:
                    #     self.screen.blit(image, tile)
                    #     tile = tile.move(tile.width, 0)

                    pass
                elif obj.type == 5:
                    pass
                elif obj.type == 6:
                    pass
                elif obj.type == 7:
                    pass

                # # Type
                # if obj.type == 0:  # Static image
                #     self.screen.blit(image, rect)
                # elif obj.type in horizontal:  # Copied horizontally
                #     tile = rect.copy()
                #     while tile.x > -tile.width:  # TODO: Don't do this the lazy way
                #         self.screen.blit(image, tile)
                #         tile = tile.move(-tile.width, 0)
                #     tile = rect.copy()
                #     while tile.x < w:
                #         self.screen.blit(image, tile)
                #         tile = tile.move(tile.width, 0)
                # elif obj.type in vertical:  # Copied vertically
                #     tile = rect.copy()
                #     while tile.y > -tile.height:  # TODO: Don't do this the lazy way
                #         self.screen.blit(image, tile)
                #         tile = tile.move(0, -tile.height)
                #     tile = rect.copy()
                #     while tile.y < h:
                #         self.screen.blit(image, tile)
                #         tile = tile.move(0, tile.height)

            except Exception as e:
                print(e)
                continue

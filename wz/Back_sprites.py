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

                # First set sprite rect as width and height
                rect = sprite.get_rect()
                obj.width = rect.width
                obj.height = rect.height

                # Set other defaults
                obj.center_x = 0
                obj.center_y = 0
                obj.z = 0

                # Get additional properties
                try:

                    # Extract data
                    object_data = self.xml[name].objects
                    back_data = object_data['back']

                    # Set data
                    data = back_data[obj.no]
                    obj.width = int(data['width'])
                    obj.height = int(data['height'])
                    obj.center_x = int(data['x'])
                    obj.center_y = int(data['y'])
                    obj.z = int(data['z'])

                except:
                    pass

                # Add to list
                objects.append(obj)

            except:
                print('Error while loading back')
                continue

        self.objects = objects

    def calculate_x(self, x, rx, dx, z):
        return float(rx * (dx + z) / 100) + x + z

    def calculate_y(self, y, ry, dy, z):
        return float(ry * (dy + z) / 100) + y + z

    def update(self):
        pass
        # horizontal = [4, 6]
        # vertical = [5, 7]
        # frame_ticks = 1
        # for obj in self.objects:
        #     if obj.type in horizontal and obj.width > 0:
        #         obj.frame_offset += obj.rx / frame_ticks
        #         obj.frame_offset %= obj.width
        #     if obj.type in vertical and obj.height > 0:
        #         obj.frame_offset += obj.ry / frame_ticks
        #         obj.frame_offset %= obj.height

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

                # Center offset
                rect.topleft = (-obj.center_x, -obj.center_y)

                # Image and camera offset
                dx = offset.x if offset else 0
                dy = offset.y if offset else 0
                x = self.calculate_x(obj.x, obj.rx, dx, 0.5 * w)
                y = self.calculate_y(obj.y, obj.ry, dy, 0.5 * h)
                rect = rect.move(x, y)

                # Image flip
                if obj.f > 0:
                    image = pygame.transform.flip(image, True, False)

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
                    delta = obj.cx if obj.cx > 0 else obj.width
                    if delta > 0:
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

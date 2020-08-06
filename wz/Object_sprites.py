import os
import pygame

from Object_xml import Object_xml
from Object_obj import Object_obj


vec = pygame.math.Vector2


class Object_sprites(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.xml = {}
        self.xml_done = []
        self.sprites = {}
        self.objects = []

    def load_xml(self, name, path):

        # Check if xml has already been loaded before
        if name in self.xml:
            print('{} was already loaded.'.format(name))
            return

        # Load and parse the xml
        file = "{}/data/Obj/{}.img.xml".format(path, name)
        self.xml[name] = Object_xml()
        self.xml[name].open(file)
        self.xml[name].parse_root()

    def load_sprites(self, name, path):

        # Check if xml has finished loading
        if name not in self.xml or not self.xml[name].objects:
            print('{} was not loaded yet.'.format(name))
            return

        # Load sprites for a given xml file
        xml = self.xml[name]
        for tag, objects in xml.objects.items():
            for item_name, item_array in objects.items():
                for canvases_index in range(0, len(item_array)):

                    # Create key
                    key = "{}.{}.{}.{}".format(
                        name, tag, item_name, str(canvases_index))

                    # Get a list of images for the key
                    images = []
                    for index in range(0, 20):  # Num frames
                        file = '{}/data/Obj/{}/{}.{}.{}.{}.png'.format(
                            path, xml.name, tag, item_name, str(canvases_index), str(index))
                        if os.path.isfile(file):
                            image = pygame.image.load(file).convert_alpha()
                            images.append(image)
                        else:
                            break

                    # Add images for the key (This will overrite any existing keys!)
                    self.sprites[key] = images

    def clear_objects(self):
        self.objects.clear()

    def load_objects(self, name, object_instances):

        # Check if xml has finished loading
        if name not in self.xml or not self.xml[name].objects:
            print('{} was not loaded yet.'.format(name))
            return

        # Go through instances list and add
        for instance in object_instances:
            try:

                # Build object
                obj = Object_obj()

                # Required properties
                obj.oS = instance['oS']
                obj.l0 = instance['l0']
                obj.l1 = instance['l1']
                obj.l2 = instance['l2']
                obj.x = int(instance['x'])
                obj.y = int(instance['y'])
                obj.z = int(instance['z'])
                obj.f = int(instance['f'])
                obj.zM = int(instance['zM'])

                # Optional properties
                if 'r' in instance:
                    obj.r = int(instance['r'])
                if 'move' in instance:
                    obj.move = int(instance['move'])
                if 'dynamic' in instance:
                    obj.dynamic = int(instance['dynamic'])
                if 'piece' in instance:
                    piece = int(instance['piece'])

                # Get sprite by key
                key = "{}.{}.{}.{}".format(obj.oS, obj.l0, obj.l1, obj.l2)
                if key not in self.sprites:
                    print('{} was not loaded yet.'.format(key))
                    continue
                obj.sprites = self.sprites[key]

                # Explicit special case
                if obj.z:
                    obj.zM = obj.z

                # Get additional properties
                try:

                    # Set default data
                    obj.cx = 0
                    obj.cy = 0
                    obj.z = 0

                    # Extract data
                    objects = self.xml[name].objects
                    l0 = objects[obj.l0]
                    l1 = l0[obj.l1]
                    l2 = l1[int(obj.l2)]

                    # Set data
                    data = l2[0]
                    obj.cx = int(data['cx'])
                    obj.cy = int(data['cy'])
                    obj.z = int(data['z'])

                except:
                    pass

                # Add to list
                self.objects.append(obj)

            except:
                print('Error while loading objects')
                continue

        # Pre process and sort by z
        self.objects = sorted(self.objects, key=lambda k: k.zM)

    def update(self):
        for obj in self.objects:
            obj.frame_count = (obj.frame_count + 1) % 180
            n = len(obj.sprites)
            if n > 0:
                obj.frame_index = int(obj.frame_count / 10 % n)

    def blit(self, offset=None):
        for obj in self.objects:
            try:
                # Get image
                image = obj.sprites[obj.frame_index]
                rect = image.get_rect().copy()

                # Image offset
                rect.topleft = vec(-obj.cx, -obj.cy)
                rect = rect.move(obj.x, obj.y)

                # Check offset
                if offset and not rect.colliderect(offset):
                    continue

                # Image flip
                if obj.f > 0:
                    image = pygame.transform.flip(image, True, False)

                # Camera offset
                if offset:
                    rect = rect.move(-offset.x, -offset.y)

                # Draw
                self.screen.blit(image, rect)

            except:
                print('Error while drawing objects')
                continue

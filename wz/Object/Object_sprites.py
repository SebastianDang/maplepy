import os
import pygame
import traceback

from Wz.Object.Object_xml import Object_xml
from Wz.Object.Object_obj import Object_obj


vec = pygame.math.Vector2


class Object_sprites(pygame.sprite.Sprite):
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
        file = "{}/Obj/{}.img.xml".format(path, name)
        self.xml[name] = Object_xml()
        self.xml[name].open(file)
        self.xml[name].parse_root()

    def clear_objects(self):
        self.objects.clear()

    def load_objects(self, object_instances, path):

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

                # Check if xml has finished loading
                if obj.oS not in self.xml or not self.xml[obj.oS].objects:
                    print('{} was not loaded yet.'.format(obj.oS))
                    continue

                # Extract data
                objects = self.xml[obj.oS].objects
                l0 = objects[obj.l0]
                l1 = l0[obj.l1]
                l2 = l1[int(obj.l2)]

                # Get information for each frame
                for item in l2:
                    if 'x' in item:
                        obj.center_x.append(int(item['x']))
                    if 'y' in item:
                        obj.center_y.append(int(item['y']))
                    if 'z' in item:
                        obj.z.append(int(item['z']))
                    if 'delay' in item:
                        obj.delay.append(int(item['delay']))

                # Load sprites
                obj.sprites = self.load_sprites(
                    path, obj.oS, obj.l0, obj.l1, obj.l2)

                # Explicit special case
                instance_z = int(instance['z'])
                for z in obj.z:
                    obj.zM = instance_z

                # Add to list
                self.objects.append(obj)

            except:
                traceback.print_exc()
                # print('Error while loading objects')
                continue

        # Pre process and sort by z
        self.objects = sorted(self.objects, key=lambda k: k.zM)

    def load_sprites(self, path, oS, l0, l1, l2):

        # Get a list of images for the key
        images = []
        for index in range(0, 20):  # Num frames
            file = '{}/Obj/{}.img/{}.{}.{}.{}.png'.format(
                path, oS, l0, l1, l2, str(index))
            if os.path.isfile(file):
                image = pygame.image.load(file).convert_alpha()
                images.append(image)
            else:
                break

        # Create key
        key = "{}.{}.{}.{}".format(
            oS, l0, l1, l2)

        # Store images
        self.sprites[key] = images

        # Return list of images
        return images

    def update(self):
        for obj in self.objects:
            obj.frame_count = (obj.frame_count + 1) % 180
            n = len(obj.sprites)
            if n > 0:
                obj.frame_index = int(obj.frame_count / 20 % n)

    def blit(self, offset=None):
        for obj in self.objects:
            try:
                # Was not able to load sprites
                if not obj.sprites:
                    continue

                # Get image
                image = obj.sprites[obj.frame_index]
                rect = image.get_rect().copy()

                # Get offets
                center_x = obj.center_x[obj.frame_index]
                center_y = obj.center_y[obj.frame_index]

                # Image offset
                rect.topleft = vec(-center_x, -center_y)
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

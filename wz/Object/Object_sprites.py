import os
import pygame

from Wz.Object.Object_xml import Object_xml
from Wz.Info.Object import Object
from Wz.Info.Canvas import Canvas
from Wz.Info.Foothold import Foothold


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

    def load_sprites(self, path, oS, l0, l1, l2):

        # Create key
        key = "{}.{}.{}.{}".format(
            oS, l0, l1, l2)

        # Check if sprites are already loaded
        if key in self.sprites:
            return self.sprites[key]

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

        # Store images
        self.sprites[key] = images

        # Return list of images
        return images

    def clear_objects(self):
        self.objects.clear()

    def load_objects(self, object_instances, path):

        # Go through instances list and add
        for instance in object_instances:
            try:

                # Build object
                obj = Object()

                # Required properties
                obj.x = int(instance['x'])
                obj.y = int(instance['y'])
                obj.oS = instance['oS']
                obj.l0 = instance['l0']
                obj.l1 = instance['l1']
                obj.l2 = instance['l2']
                obj.zM = int(instance['zM'])
                obj.f = int(instance['f'])

                # Optional properties
                if 'r' in instance:
                    obj.r = int(instance['r'])
                if 'move' in instance:
                    obj.move = int(instance['move'])
                if 'dynamic' in instance:
                    obj.dynamic = int(instance['dynamic'])
                if 'piece' in instance:
                    obj.piece = int(instance['piece'])

                # Load sprites
                sprites = self.load_sprites(
                    path, obj.oS, obj.l0, obj.l1, obj.l2)

                # Check if xml has finished loading
                if obj.oS not in self.xml or not self.xml[obj.oS].objects:
                    print('{} was not loaded yet.'.format(obj.oS))
                    continue

                # Get additional properties
                objects = self.xml[obj.oS].objects
                l0 = objects[obj.l0]
                l1 = l0[obj.l1]
                l2 = l1[int(obj.l2)]

                # Create canvases
                for i in range(0, len(sprites)):

                    # Get sprite info
                    sprite = sprites[i]
                    w, h = sprite.get_size()

                    # Get xml info
                    item = l2[i]
                    x = int(item['x'])
                    y = int(item['y'])
                    z = int(item['z'])
                    delay = int(item['delay']) if 'delay' in item else 0

                    # Create a canvas object
                    canvas = Canvas(sprite, w, h, x, y, z)
                    canvas.delay = delay
                    obj.canvas.append(canvas)

                    # Add footholds
                    if 'extended' in item:
                        for foothold in item['extended']:
                            fx = int(foothold['x'])
                            fy = int(foothold['y'])
                            foothold = Foothold(fx, fy)
                            canvas.footholds.append(foothold)

                    # Explicit special case
                    if 'z' in instance:
                        obj.zM = int(instance['z'])

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
            n = len(obj.canvas)
            if n > 0:
                obj.canvas_index = int(obj.frame_count / 20 % n)

    def blit(self, offset=None):
        for obj in self.objects:
            try:
                # Get canvas
                canvas = obj.get_canvas()

                # Extract image
                image = canvas.get_image(obj.f)  # Flip
                rect = canvas.get_center_rect(obj.x, obj.y)

                # Check offset
                if offset and not rect.colliderect(offset):
                    continue

                # Camera offset
                if offset:
                    rect = rect.move(-offset.x, -offset.y)

                # Draw
                self.screen.blit(image, rect)

                # Draw footholds
                obj.draw_footholds(self.screen, offset)

            except:
                print('Error while drawing objects')
                continue

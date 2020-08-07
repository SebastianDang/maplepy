import os
import pygame

from Wz.Xml.Xml import Layer, Xml
from Wz.Info.Instance import Instance
from Wz.Info.Canvas import Canvas
from Wz.Info.Foothold import Foothold


vec = pygame.math.Vector2


class Object_sprites(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.xml = {}
        self.sprites = {}
        self.objects = pygame.sprite.LayeredUpdates()

    def load_xml(self, name, path):

        # Check if xml has already been loaded before
        if name in self.xml:
            print('{} was already loaded.'.format(name))
            return

        # Load and parse the xml
        file = "{}/Obj/{}.img.xml".format(path, name)
        self.xml[name] = Xml()
        self.xml[name].open(file)
        self.xml[name].parse_root(Layer.TAGS)

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

    def load_objects(self, object_instances, path):

        # Go through instances list and add
        for instance in object_instances:
            try:

                # Build object
                obj = Instance()

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
                    z = int(item['z']) if 'z' in item else 0
                    delay = int(item['delay']) if 'delay' in item else 120

                    # Create a canvas object
                    canvas = Canvas(sprite, w, h, x, y, z)

                    # Set delay
                    canvas.set_delay(delay)

                    # Add footholds
                    if 'extended' in item:
                        for foothold in item['extended']:
                            fx = int(foothold['x'])
                            fy = int(foothold['y'])
                            canvas.add_foothold(Foothold(fx, fy))

                    # Flip
                    if obj.f > 0:
                        canvas.flip()

                    # Add to object
                    obj.add_canvas(canvas)

                    # Explicit special case
                    if 'z' in instance:
                        obj.update_layer(int(instance['z']))

                # Add to list
                self.objects.add(obj)

            except:
                print('Error while loading objects')
                continue


    def update(self):
        for obj in self.objects:
            obj.update()

    def blit(self, surface, offset=None):
        if not self.objects:
            return
        for obj in self.objects:
            try:

                # Camera offset
                if offset:
                    rect = obj.rect.move(-offset.x, -offset.y)

                # Draw
                surface.blit(obj.image, rect)

            except:
                continue

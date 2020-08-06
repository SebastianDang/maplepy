import os
import pygame

from Object_xml import Object_xml
from Object_obj import Object_obj


vec = pygame.math.Vector2


class Object_sprites(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.xml = None
        self.sprites = {}
        self.objects = None

    def load_xml(self, xml):
        self.xml = Object_xml()
        self.xml.open(xml)
        self.xml.parse_root()

    def load_sprites(self, path):
        if not self.xml:
            return
        sprites = {}
        for tag, objects in self.xml.objects.items():
            for item_name, item_array in objects.items():
                for canvases_index in range(0, len(item_array)):
                    images = []
                    for index in range(0, 20):  # Max num of frames
                        file = '{}/data/Obj/{}/{}.{}.{}.{}.png'.format(
                            path, self.xml.name, tag, item_name, str(canvases_index), str(index))
                        if os.path.isfile(file):
                            image = pygame.image.load(file).convert_alpha()
                            images.append(image)
                        else:
                            break
                    key = "{}.{}.{}".format(
                        tag, item_name, str(canvases_index))
                    sprites[key] = images
        self.sprites = sprites

    def load_objects(self, object_instances):
        objects = []
        for instance in object_instances:
            try:
                # Instance properties
                oS = instance['oS']
                l0 = instance['l0']
                l1 = instance['l1']
                l2 = instance['l2']
                x = int(instance['x'])
                y = int(instance['y'])
                z = int(instance['z'])
                f = int(instance['f'])
                zM = int(instance['zM'])
                r = int(instance['r'])
                move = int(instance['move'])
                dynamic = int(instance['dynamic'])
                piece = int(instance['piece'])
                # Special case
                if oS not in self.xml.name:
                    continue
                # Object sprite
                sprites = self.sprites["{}.{}.{}".format(l0, l1, l2)]
                sprite = sprites[0]  # start with 0
                # Build object
                obj = Object_obj()
                obj.l0 = l0
                obj.l1 = l1
                obj.l2 = l2
                obj.x = x
                obj.y = y
                obj.z = z
                obj.f = f
                obj.zM = zM
                obj.r = r
                obj.move = move
                obj.dynamic = dynamic
                obj.piece = piece
                obj.sprite = sprite
                # Explicit special case
                if obj.z:
                    obj.zM = obj.z
                # Add to list
                objects.append(obj)

            except:
                print('Error while loading objects')
                continue
        # Pre process and sort by z
        objects = sorted(objects, key=lambda k: k.zM)
        self.objects = objects

    def update(self):
        pass

    def blit(self, offset=None):

        for obj in self.objects:
            try:
                # Get image
                image = obj.sprite
                rect = image.get_rect().copy()

                # Image offset
                rect.center = vec(obj.x, obj.y)

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

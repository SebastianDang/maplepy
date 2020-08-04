import os
import sys
import pygame
from map_wz import *
vec = pygame.math.Vector2


class map_wz_sprite(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.map_wz = None
        self.images = {}

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
                path = './img/{}/{}.{}.png'.format(n, 'back', str(i))
                if os.path.isfile(path):
                    image = pygame.image.load(path).convert_alpha()
                    images.append(image)
                else:
                    break
            self.images[n] = images

    def update(self):
        pass

    def blit(self, offset=None):

        # Render backgroundF
        for bg in self.map_wz.bg:
            try:
                bS = bg['bS']
                no = int(bg['no'])
                x = int(bg['cx'])
                y = int(bg['cy'])
                t = int(bg['type'])

                # Get image
                images = self.images[bS]
                image = images[no]

                # Image offset
                rect = image.get_rect().copy().move(x, y)

                # Type
                if t == 0:  # Static image
                    if offset:
                        rect = rect.move(-offset.x, -offset.y)
                    self.screen.blit(image, rect)
                elif t == 1:  # Copied horizontally
                    w, h = pygame.display.get_surface().get_size()
                    while rect.x < w:
                        self.screen.blit(image, rect)
                        rect = rect.move(rect.width, 0)
                elif t == 2:  # Copied vertically
                    w, h = pygame.display.get_surface().get_size()
                    while rect.y < h:
                        self.screen.blit(image, rect)
                        rect = rect.move(0, rect.height)
                elif t == 4:  # Scrolls and copied horizontally
                    if offset:
                        rect = rect.move(-offset.x, -offset.y)
                    w, h = pygame.display.get_surface().get_size()
                    while rect.x < w:
                        self.screen.blit(image, rect)
                        rect = rect.move(rect.width, 0)
                else:
                    if offset:
                        rect = rect.move(-offset.x, -offset.y)
                    self.screen.blit(image, rect)

            except:
                continue


if __name__ == "__main__":
    print(map_wz_sprite.__name__)
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    cam = pygame.Rect(0, 0, 1920, 1080)
    m = map_wz_sprite(screen)
    m.load_wz('./xml/100000000.xml')  # Henesys
    m.load_bg_images()
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

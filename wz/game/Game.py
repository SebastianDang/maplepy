import pygame
from wz.map.MapDisplay import MapDisplay


class Game():
    def __init__(self, w, h):

        pygame.init()

        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((w, h))
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.path = '.'
        self.running = False

        self.map = MapDisplay(self.screen)

    def set_path(self, path):
        self.path = path
        self.map.path = path

    def load(self):
        self.map.load_map('000010000')  # Maple Tree Hill
        # self.map.load_map('100000000')  # Henesys

    def handle_events(self):

        # Handle pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.event.clear()
                self.running = False

        # Empty
        pygame.event.pump()

    def handle_inputs(self):
        speed = 10
        inputs = pygame.key.get_pressed()
        if inputs[pygame.K_UP]:
            self.map.view = self.map.view.move(0, -speed)
        if inputs[pygame.K_DOWN]:
            self.map.view = self.map.view.move(0, speed)
        if inputs[pygame.K_LEFT]:
            self.map.view = self.map.view.move(-speed, 0)
        if inputs[pygame.K_RIGHT]:
            self.map.view = self.map.view.move(speed, 0)
        if inputs[pygame.K_r]:
            self.map.view.update(0, 0)

    def run(self):
        self.running = True
        while self.running:

            self.handle_events()

            self.handle_inputs()

            self.map.update()

            self.screen.fill((0, 0, 0))
            self.map.blit()

            pygame.display.update()

            self.clock.tick(self.fps)

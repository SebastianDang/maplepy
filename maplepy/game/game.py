import pygame

from maplepy.config import Config
from maplepy.ui.loaddisplay import LoadDisplay
from maplepy.map.mapdisplay import MapDisplay

DISPLAY_LOADING = 0
DISPLAY_MAP = 1


class Game():

    def __init__(self, config_file):

        # Start pygame
        pygame.init()

        # Config
        self.config = Config.instance()
        self.config.init(config_file)
        self.width = self.config['width']
        self.height = self.config['height']
        self.path = self.config['asset_path']
        self.maps = self.config['maps']

        # Create pygame objects
        icon = pygame.image.load(self.config['icon'])
        pygame.display.set_icon(icon)
        pygame.display.set_caption(self.config['caption'])
        self.screen = pygame.display.set_mode(
            (self.width, self.height), pygame.HWACCEL)
        self.clock = pygame.time.Clock()

        # Create displays
        self.displays = {}
        self.displays[DISPLAY_LOADING] = LoadDisplay(self.screen, self.path)
        self.displays[DISPLAY_MAP] = MapDisplay(self.screen, self.path)

        # Game state
        self.displays_state = DISPLAY_LOADING
        self.running = False
        self.fps = 60
        self.input_blocker = {}
        self.map_index = 0

    def handle_events(self):

        # Handle pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.event.clear()
                self.running = False

        # Empty
        pygame.event.pump()

    def handle_inputs(self):

        # Tmp
        speed = 4

        # Check input keys
        inputs = pygame.key.get_pressed()
        if inputs[pygame.K_UP]:
            if self.displays_state == 1:
                self.displays[1].view = self.displays[1].view.move(0, -speed)
        if inputs[pygame.K_DOWN]:
            if self.displays_state == 1:
                self.displays[1].view = self.displays[1].view.move(0, speed)
        if inputs[pygame.K_LEFT]:
            if self.displays_state == 1:
                self.displays[1].view = self.displays[1].view.move(-speed, 0)
        if inputs[pygame.K_RIGHT]:
            if self.displays_state == 1:
                self.displays[1].view = self.displays[1].view.move(speed, 0)
        if inputs[pygame.K_RETURN]:
            if pygame.K_RETURN not in self.input_blocker:
                self.input_blocker[pygame.K_RETURN] = 60
                if self.displays_state == DISPLAY_MAP:
                    self.map_index = (self.map_index + 1) % len(self.maps)
                    self.displays[DISPLAY_MAP].load_map(
                        self.maps[self.map_index])
                    self.displays_state = DISPLAY_MAP

        # Input key handling to prevent repeated keys
        input_blocker_removal = []
        for key, delay in self.input_blocker.items():
            self.input_blocker[key] = delay - 1
            if self.input_blocker[key] <= 0:
                input_blocker_removal.append(key)

        # Remove from list
        for key in input_blocker_removal:
            self.input_blocker.pop(key, None)

    def run(self):

        # Set current display
        self.displays[DISPLAY_LOADING].load_images()
        self.displays_state = DISPLAY_LOADING
        loading = 60

        # Main loop
        self.running = True
        while self.running:

            if loading:
                loading -= 1
            if self.displays_state == DISPLAY_LOADING and not loading:
                self.displays[DISPLAY_MAP].load_map(self.maps[self.map_index])
                self.displays_state = DISPLAY_MAP

            self.handle_events()
            self.handle_inputs()
            self.screen.fill((0, 0, 0))
            self.displays[self.displays_state].update()
            self.displays[self.displays_state].blit()
            pygame.display.update()
            self.clock.tick(self.fps)

import pygame

from maplepy.config import Config
from maplepy.ui.loaddisplay import LoadDisplay
from maplepy.xml.displayxml import DisplayXml
from maplepy.nx.displaynx import DisplayNx

CAMERA_SPEED = 4
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
        self.displays[DISPLAY_LOADING] = LoadDisplay(
            self.width, self.height, self.path)
        self.displays[DISPLAY_MAP] = DisplayNx(
            self.width, self.height, self.path)

        # Game state
        self.displays_state = DISPLAY_LOADING
        self.running = False
        self.fps = 60
        self.input_blocker = {}
        self.map_index = 0

        # Debugging tools TODO: Remove #
        self.typing = False
        self.text = ''
        self.font = pygame.font.Font(None, 32)
        # Debugging tools TODO: Remove #

    def handle_events(self):

        # Handle pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.event.clear()
                self.running = False

            # Debugging tools TODO: Remove #
            if event.type == pygame.KEYDOWN:
                if self.typing:
                    if event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    elif event.key == pygame.K_RETURN:
                        # Pass text to map loader
                        self.displays[DISPLAY_MAP].load_map(self.text)
                        self.typing = False
                        self.text = ''
                    else:
                        self.text += event.unicode
                if event.key == pygame.K_BACKQUOTE:
                    self.typing = not self.typing
                    self.text = ''
            # Debugging tools TODO: Remove #

        # Empty
        pygame.event.pump()

    def handle_inputs(self):

        # Get view
        view = self.displays[DISPLAY_MAP].view

        # Mouse input
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        # Check input keys
        inputs = pygame.key.get_pressed()
        if inputs[pygame.K_UP]:
            if self.displays_state == DISPLAY_MAP:
                self.displays[DISPLAY_MAP].move_view(0, -CAMERA_SPEED)
        if inputs[pygame.K_DOWN]:
            if self.displays_state == DISPLAY_MAP:
                self.displays[DISPLAY_MAP].move_view(0, CAMERA_SPEED)
        if inputs[pygame.K_LEFT]:
            if self.displays_state == DISPLAY_MAP:
                self.displays[DISPLAY_MAP].move_view(-CAMERA_SPEED, 0)
        if inputs[pygame.K_RIGHT]:
            if self.displays_state == DISPLAY_MAP:
                self.displays[DISPLAY_MAP].move_view(CAMERA_SPEED, 0)

        # Cycle through maps
        if inputs[pygame.K_TAB]:
            if pygame.K_TAB not in self.input_blocker:
                self.input_blocker[pygame.K_TAB] = 60
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

            # Handle pygame events
            self.handle_events()

            # Handle inputs
            self.handle_inputs()

            # Clear screen
            self.screen.fill((0, 0, 0))

            # Render environment
            if self.displays[self.displays_state].loaded:

                # Displays
                self.displays[self.displays_state].update()
                self.displays[self.displays_state].blit(self.screen)

            # Debugging tools TODO: Remove #
            if self.typing:
                text = self.font.render('console:{}'.format(
                    self.text), True, (255, 255, 255))
                self.screen.blit(text, (0, 0))
            # Debugging tools TODO: Remove #

            # Update
            pygame.display.update()
            self.clock.tick(self.fps)

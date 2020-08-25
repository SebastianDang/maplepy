import threading
import pygame

from maplepy.config import Config
from maplepy.ui.loaddisplay import LoadDisplay
from maplepy.xml.displayxml import DisplayXml
from maplepy.nx.displaynx import DisplayNx
from maplepy.display.console import Console

CAMERA_SPEED = 4
DISPLAY_LOADING = 0
DISPLAY_MAP = 1


class Game():

    def __init__(self, config_file):

        # Start pygame
        pygame.mixer.pre_init(22050, -16, 2)
        pygame.init()

        # Config
        self.config = Config.instance()
        self.config.init(config_file)
        self.width = self.config['width']
        self.height = self.config['height']
        self.path = self.config['asset_path']
        self.map = self.config['map']

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
        self.thread = None
        self.state = DISPLAY_MAP
        self.running = False
        self.fps = 60
        self.input_blocker = {}

        # Console
        self.typing = False
        self.text = ''
        self.console = Console(200, 400)

    def get_state(self):

        if self.thread.isAlive():
            return DISPLAY_LOADING
        else:
            return self.state

    def process_command(self, text):

        # Parse text
        command = text.split()
        if len(command) < 1:
            return

        # Process command
        try:
            cmd = command[0].lower()
            if cmd == 'map':
                fn = self.displays[DISPLAY_MAP].load_map
                args = (command[1],)
                self.thread = threading.Thread(target=fn, args=args)
                self.thread.start()
        except:
            pass

    def handle_events(self):

        # Handle pygame events
        for event in pygame.event.get():

            # Quit application
            if event.type == pygame.QUIT:
                pygame.event.clear()
                self.running = False

            # Console input
            if event.type == pygame.KEYDOWN:
                if self.typing:
                    if event.key == pygame.K_ESCAPE:
                        self.typing = False
                        self.text = ''
                        pygame.key.set_repeat()
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    elif event.key == pygame.K_RETURN:
                        self.process_command(self.text)
                        self.typing = False
                        self.text = ''
                    else:
                        self.text += event.unicode
                elif event.key == pygame.K_BACKQUOTE:
                    self.typing = True
                    self.text = ''
                    pygame.key.set_repeat(300)

        # Empty
        pygame.event.pump()

    def handle_inputs(self):

        # Get current state
        state = self.get_state()

        # # Mouse input
        # mouse_x, mouse_y = pygame.mouse.get_pos()
        # mouse_input = pygame.mouse.get_pressed()

        # Key input
        key_input = pygame.key.get_pressed()
        if key_input[pygame.K_UP]:
            if state == DISPLAY_MAP:
                self.displays[DISPLAY_MAP].move_view(0, -CAMERA_SPEED)
        if key_input[pygame.K_DOWN]:
            if state == DISPLAY_MAP:
                self.displays[DISPLAY_MAP].move_view(0, CAMERA_SPEED)
        if key_input[pygame.K_LEFT]:
            if state == DISPLAY_MAP:
                self.displays[DISPLAY_MAP].move_view(-CAMERA_SPEED, 0)
        if key_input[pygame.K_RIGHT]:
            if state == DISPLAY_MAP:
                self.displays[DISPLAY_MAP].move_view(CAMERA_SPEED, 0)

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

        # Setup loading display
        self.displays[DISPLAY_LOADING].load_images()

        # Setup initial map
        self.process_command('map {}'.format(self.map))

        # Main loop
        self.running = True
        while self.running:

            # Get current state
            state = self.get_state()

            # Handle pygame events
            self.handle_events()

            # Handle inputs
            self.handle_inputs()

            # Clear screen
            self.screen.fill((0, 0, 0))

            # Render environment
            self.displays[state].update()
            self.displays[state].blit(self.screen)

            # Console
            if self.typing:
                self.console.blit(self.screen, self.text)

            # Update
            pygame.display.update()
            self.clock.tick(self.fps)

import pygame

from maplepy.config import Config
from maplepy.ui.loaddisplay import LoadDisplay
from maplepy.map.mapdisplay import MapDisplay
from maplepy.game.square import Square

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
        self.displays[DISPLAY_MAP] = MapDisplay(
            self.width, self.height, self.path)

        # Game state
        self.displays_state = DISPLAY_LOADING
        self.running = False
        self.fps = 60
        self.input_blocker = {}
        self.map_index = 0

        # Player
        self.player = Square()

    def handle_events(self):

        # Handle pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.event.clear()
                self.running = False

        # Empty
        pygame.event.pump()

    def handle_inputs(self):

        # Get view
        view = self.displays[DISPLAY_MAP].view

        # Mouse input
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if mouse_click[0]:

            if view:
                self.player.place(mouse_x + view.x, mouse_y + view.y)
            else:
                self.player.place(mouse_x, mouse_y)

        # Check input keys
        inputs = pygame.key.get_pressed()
        if inputs[pygame.K_w]:
            if self.displays_state == DISPLAY_MAP:
                self.displays[DISPLAY_MAP].view = view.move(0, -CAMERA_SPEED)
        if inputs[pygame.K_s]:
            if self.displays_state == DISPLAY_MAP:
                self.displays[DISPLAY_MAP].view = view.move(0, CAMERA_SPEED)
        if inputs[pygame.K_a]:
            if self.displays_state == DISPLAY_MAP:
                self.displays[DISPLAY_MAP].view = view.move(-CAMERA_SPEED, 0)
        if inputs[pygame.K_d]:
            if self.displays_state == DISPLAY_MAP:
                self.displays[DISPLAY_MAP].view = view.move(CAMERA_SPEED, 0)

        # Debug: cycle through maps
        if inputs[pygame.K_TAB]:
            if pygame.K_TAB not in self.input_blocker:
                self.input_blocker[pygame.K_TAB] = 60
                if self.displays_state == DISPLAY_MAP:
                    self.map_index = (self.map_index + 1) % len(self.maps)
                    self.displays[DISPLAY_MAP].load_map(
                        self.maps[self.map_index])
                    self.displays_state = DISPLAY_MAP

        # Player movement
        if inputs[pygame.K_LEFT]:
            self.player.on_left()
        if inputs[pygame.K_RIGHT]:
            self.player.on_right()
        if inputs[pygame.K_UP]:
            self.player.on_up()
        if inputs[pygame.K_DOWN]:
            self.player.on_down()

        # Input key handling to prevent repeated keys
        input_blocker_removal = []
        for key, delay in self.input_blocker.items():
            self.input_blocker[key] = delay - 1
            if self.input_blocker[key] <= 0:
                input_blocker_removal.append(key)

        # Remove from list
        for key in input_blocker_removal:
            self.input_blocker.pop(key, None)

    def handle_player_collisions(self):

        collisions = []

        sprite_layers = self.displays[DISPLAY_MAP].map_sprite_layers
        for sprite_layer in sprite_layers:
            collisions += pygame.sprite.spritecollide(
                self.player, sprite_layer.sprites, False)

        view = self.displays[DISPLAY_MAP].view

        if collisions:
            for sprite in collisions:
                if sprite.get_footholds():
                    sprite.draw_footholds(self.screen, view)

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
            self.player.update()

            # Clear screen
            self.screen.fill((0, 0, 0))

            # Render environment
            if self.displays[self.displays_state].loaded:

                # Displays
                self.displays[self.displays_state].update()
                self.displays[self.displays_state].blit(self.screen)

            # Player
            self.handle_player_collisions()

            # Render player
            if self.displays[self.displays_state].loaded and self.displays_state == DISPLAY_MAP:

                # Player
                self.player.blit(self.screen, self.displays[DISPLAY_MAP].view)

            # Update
            pygame.display.update()
            self.clock.tick(self.fps)

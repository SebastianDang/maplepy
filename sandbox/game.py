import pygame
from config import *
from world import *
from player import *
from utils import *


class Game:

    def __init__(self):

        print('Game:', 'Created', '.')

        # Variables
        self.running = False
        self.screen = None
        self.caption = None
        self.width = None
        self.height = None
        self.fps = None
        self.cam = None
        self.cam_dx = None
        self.cam_dy = None
        self.clock = None
        self.flags = pygame.DOUBLEBUF
        self.key_delay = {}

        # Objects
        self.player = None
        self.entities = {}

    def init(self):

        print('Game:', 'Starting', '...')

        # Config
        config = Config.instance()

        # Get variables from config
        self.caption = config['caption']
        self.width = config['width']
        self.height = config['height']
        self.fps = config['fps']
        self.cam_dx = config['cam_dx']
        self.cam_dy = config['cam_dy']
        self.maps = config['maps']

        # Update game
        pygame.display.set_caption(self.caption)
        self.screen = pygame.display.set_mode(
            (self.width, self.height), self.flags)
        self.cam = pygame.Rect(0, 0, self.width, self.height)
        self.clock = pygame.time.Clock()

    def load_player(self):

        print('Game:', 'Loading player', '...')

        self.player = Player(self.screen)
        self.player.place(512, 300)

    def clear_map(self):

        print('Game:', 'Clearing map', '...')

        self.entities.clear()

    def load_map(self, index):

        print('Game:', 'Loading map', '...')

        # Load map by index
        if index not in range(0, len(self.maps)):
            print('Game', 'Map does not exist!')
            return
        m = self.maps[index]

        # Properties
        bounds = pygame.Rect(
            0, 0, m['bounds']['width'], m['bounds']['height'])

        # Background
        background = Background(self.screen)
        background.init(m['background']['img'])

        # Music
        if 'music' in m:
            pygame.mixer.init()
            pygame.mixer.music.load(m['music']['file'])
            pygame.mixer.music.set_volume(m['music']['volume'])
            pygame.mixer.music.play(-1)  # Loop

        # Sprites
        sprites = pygame.sprite.Group()
        for sprite in m['sprites']:
            if sprite['type'] == 'Obstacle':
                obstacle = Obstacle(self.screen)
                obstacle.init(sprite['x'], sprite['y'],
                              sprite['width'], sprite['height'])
                if 'platform' in sprite:
                    obstacle.platform = sprite['platform']
                sprites.add(obstacle)
            if sprite['type'] == 'Portal':
                portal = Portal(self.screen)
                portal.place(sprite['x'], sprite['y'])
                portal.dest = sprite['dest']
                sprites.add(portal)

        # Add to dictionary
        self.entities['background'] = background
        self.entities['bounds'] = bounds
        self.entities['sprites'] = sprites

    def handle_camera(self):

        bounds = self.entities['bounds']
        self.cam.center = (round(self.player.pos.x+self.cam_dx),
                           round(self.player.pos.y+self.cam_dy))
        self.cam = self.cam.clamp(bounds)  # Clamp inside bounds rect

    def handle_events(self):

        # Get events
        events = pygame.event.get()

        # Handle pygame events
        for event in events:
            if event.type == pygame.QUIT:
                pygame.event.clear()
                self.running = False

        pygame.event.pump()

    def handle_inputs(self):

        # Get inputs
        inputs = pygame.key.get_pressed()

        # Player pressed up on portal
        if inputs[pygame.K_UP] and self.player.portal:
            if self.player.portal.dest in range(0, len(self.maps)):
                self.clear_map()
                self.load_map(self.player.portal.dest)
                self.player.place_fall(
                    self.player.pos.x, self.player.portal.rect.top)
                self.player.portal = None

        # Player prone on and off
        if inputs[pygame.K_DOWN]:
            self.player.on_down()
        if not inputs[pygame.K_DOWN]:
            self.player.off_down()

        # Player movement
        if inputs[pygame.K_LEFT]:
            self.player.on_left()
        if inputs[pygame.K_RIGHT]:
            self.player.on_right()

        # Player jump
        if inputs[pygame.K_LALT]:
            self.player.on_jump()

        # Player attack
        if inputs[pygame.K_LCTRL]:
            self.player.on_attack()

        # Input key handling to prevent repeated keys
        key_delay_removal = []
        for key, delay in self.key_delay.items():
            self.key_delay[key] = delay - 1
            if self.key_delay[key] <= 0:
                key_delay_removal.append(key)

        # Remove from list
        for key in key_delay_removal:
            self.key_delay.pop(key, None)

    def handle_collisions(self, player):

        # Off collision detection
        if player.floor and rect_outside(player.rect, player.floor.rect):
            player.floor = None
            player.on_fall()

        # Collision detection
        for entity in self.entities['sprites']:
            if isinstance(entity, Obstacle):
                side, value = colliderect_info(
                    entity.rect, player.rect)
                if side:
                    # Top
                    if side == 'top' and entity.player_above:
                        player.off_jump()  # Disable falling or jumping
                        player.place(player.pos.x,
                                     player.pos.y - value)
                        player.floor = entity
                    # If platform, stop checking
                    if entity.platform:
                        continue
                    # Sides
                    if side == 'bottom':
                        player.place(player.pos.x,
                                     player.pos.y + value)
                    if side == 'left':
                        player.place(
                            player.pos.x - value, player.pos.y)
                    if side == 'right':
                        player.place(
                            player.pos.x + value, player.pos.y)
                # Keep track if the player is above this obstacle or not
                entity.player_above = rect_above(
                    player.rect, entity.rect)
            if isinstance(entity, Portal):
                side, value = colliderect_info(
                    entity.rect, player.rect)
                if side:
                    # Inside
                    if side == 'inside' or value > (entity.rect.width * 0.6):
                        player.portal = entity

    def update(self):

        # Return if not running
        if not self.running:
            return

        # Handle camera movement
        self.handle_camera()

        # Handle events
        self.handle_events()

        # Handle collisions
        self.handle_collisions(self.player)

        # Handle user input
        self.handle_inputs()

        # Handle entities
        for entity in self.entities['sprites']:
            entity.update()

        # Handle player
        self.player.update()

        # Update clock
        self.clock.tick(self.fps)

    def draw(self):

        # Render black
        self.screen.fill((0, 0, 0))

        # Draw background
        if 'background' in self.entities:
            self.entities['background'].blit(self.cam)

        # Draw entities
        for entity in self.entities['sprites']:
            if entity.rect.colliderect(self.cam):
                entity.blit(self.cam)

        # Draw player
        self.player.blit(self.cam)

        # Update display
        pygame.display.update()

import sys
import pygame
from utils import colliderect_info, rect_above, rect_outside
from config import Config
from player import Player
from world import Background, Obstacle, Portal

# Get configuration parameters
config = Config.instance()
config.init('etc/config.json')

# Get variables from config
caption = config['caption']
width = config['width']
height = config['height']
fps = config['fps']
cam_dx = config['cam_dx']
cam_dy = config['cam_dy']

# Initialize pygame
pygame.init()
pygame.display.set_caption(caption)
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
cam = pygame.Rect(0, 0, width, height)
is_loading = None
key_delay = {}

# Create player
player = Player(screen)
player.place(512, 300)

# Add sprites
entities = []
entities_index = 0
for m in config['maps']:
    params = {}
    # Properties
    bounds = pygame.Rect(0, 0, m['bounds']['width'], m['bounds']['height'])
    # Sprites
    sprites = pygame.sprite.Group()
    for sprite in m['sprites']:
        if sprite['type'] == 'Background':
            background = Background(screen)
            background.init(sprite['img'])
            sprites.add(background)
        if sprite['type'] == 'Obstacle':
            obstacle = Obstacle(screen)
            obstacle.init(sprite['x'], sprite['y'],
                          sprite['width'], sprite['height'])
            if 'platform' in sprite:
                obstacle.platform = sprite['platform']
            sprites.add(obstacle)
        if sprite['type'] == 'Portal':
            portal = Portal(screen)
            portal.place(sprite['x'], sprite['y'])
            portal.dest = sprite['dest']
            sprites.add(portal)
    sprites.add(player)
    # Add to dictionary
    params['bounds'] = bounds
    params['sprites'] = sprites
    # Add dictionary to list
    entities.append(params)

is_running = True
while is_running:

    # Render black
    screen.fill((0, 0, 0))

    # Adjust camera
    bounds = entities[entities_index]['bounds']
    cam.center = (round(player.pos.x+cam_dx), round(player.pos.y+cam_dy))
    cam = cam.clamp(bounds)  # Clamp inside bounds rect

    # # Loading
    # if is_loading:
    #     # Update variable
    #     is_loading -= 1
    #     if is_loading <= 0:
    #         is_loading = None
    #     # Update display and clock
    #     pygame.display.update()
    #     clock.tick(fps)
    #     continue

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.event.clear()
            is_running = False
            continue

    # Input key handling
    pressed_keys = pygame.key.get_pressed()
    # Player pressed up on portal
    if pressed_keys[pygame.K_UP] and player.portal:
        if player.portal.dest in range(0, len(entities)):
            entities_index = player.portal.dest
            is_loading = 10
            player.place_fall(player.pos.x, player.portal.rect.top)
    # Player prone on and off
    if pressed_keys[pygame.K_DOWN]:
        player.on_down()
    if not pressed_keys[pygame.K_DOWN]:
        player.off_down()
    # Player movement
    if pressed_keys[pygame.K_LEFT]:
        player.on_left()
    if pressed_keys[pygame.K_RIGHT]:
        player.on_right()
    # Player jump
    if pressed_keys[pygame.K_LALT]:
        player.on_jump()
    # Player attack
    if pressed_keys[pygame.K_LCTRL]:
        player.on_attack()

    # Input key handling to prevent repeated keys
    key_delay_removal = []
    for key, delay in key_delay.items():
        key_delay[key] = delay - 1
        if key_delay[key] <= 0:
            key_delay_removal.append(key)
    # Remove from list
    for key in key_delay_removal:
        key_delay.pop(key, None)

    # Reset any states for this loop
    player.portal = None

    # Off collision detection
    if player.floor and rect_outside(player.rect, player.floor.rect):
        player.floor = None
        player.on_fall()

    # Collision detection
    for entity in entities[entities_index]['sprites']:
        if isinstance(entity, Obstacle):
            # Check for collisions
            side, value = colliderect_info(entity.rect, player.rect)
            if side:
                # Top
                if side == 'top' and entity.player_above:
                    player.off_jump()  # Disable falling or jumping
                    player.place(player.pos.x, player.pos.y - value)
                    player.floor = entity
                # If platform, stop checking
                if entity.platform:
                    continue
                # Sides
                if side == 'bottom':
                    player.place(player.pos.x, player.pos.y + value)
                if side == 'left':
                    player.place(player.pos.x - value, player.pos.y)
                if side == 'right':
                    player.place(player.pos.x + value, player.pos.y)
            # Keep track if the player is above this obstacle or not
            entity.player_above = rect_above(player.rect, entity.rect)
        if isinstance(entity, Portal):
            # Check for collisions
            side, value = colliderect_info(entity.rect, player.rect)
            if side:
                # Inside
                if side == 'inside' or value > (entity.rect.width * 0.6):
                    player.portal = entity

    # Render entities
    for entity in entities[entities_index]['sprites']:
        entity.update()
        entity.blit(cam)

    # Update display and clock
    pygame.display.update()
    clock.tick(fps)

pygame.quit()

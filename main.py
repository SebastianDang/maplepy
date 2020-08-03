import sys
import pygame
from utils import colliderect_info
from config import Config
from player import Player
from world import Background, Obstacle, Portal

# Get configuration parameters
config = Config.instance()
config.init('etc/config.json')

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((config['width'], config['height']))
pygame.display.set_caption(config['caption'])
clock = pygame.time.Clock()
fps = config['fps']
is_loading = None
key_delay = {}

# Create player
player = Player(screen)
player.place(512, 510)

# Add sprites
sprite_groups = []
sprite_group_index = 0
for m in config['maps']:
    sprite_group = pygame.sprite.Group()
    for sprite in m['sprites']:
        if sprite['type'] == 'Background':
            background = Background(screen)
            background.init(sprite['img'])
            sprite_group.add(background)
        if sprite['type'] == 'Obstacle':
            obstacle = Obstacle(screen)
            obstacle.init(sprite['x'], sprite['y'],
                          sprite['width'], sprite['height'])
            sprite_group.add(obstacle)
        if sprite['type'] == 'Portal':
            portal = Portal(screen)
            portal.place(sprite['x'], sprite['y'])
            portal.dest = sprite['dest']
            sprite_group.add(portal)
    sprite_group.add(player)
    sprite_groups.append(sprite_group)

is_running = True
while is_running:

    # Render black
    screen.fill((0, 0, 0))

    # Loading
    if is_loading:
        # Update variable
        is_loading -= 1
        if is_loading <= 0:
            is_loading = None
        # Update display and clock
        pygame.display.update()
        clock.tick(fps)
        continue

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.event.clear()
            is_running = False
            continue

    # Input key handling
    pressed_keys = pygame.key.get_pressed()
    # Experimental
    if pressed_keys[pygame.K_TAB] and pygame.K_TAB not in key_delay:
        key_delay[pygame.K_TAB] = 60
        sprite_group_index = (sprite_group_index + 1) % len(sprite_groups)
    # Player pressed up on portal
    if pressed_keys[pygame.K_UP] and player.portal:
        if player.portal.dest in range(0, len(sprite_groups)):
            sprite_group_index = player.portal.dest
            is_loading = 10
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

    # Collision detection
    for entity in sprite_groups[sprite_group_index]:
        if isinstance(entity, Obstacle):
            side, value = colliderect_info(entity.rect, player.rect)
            if side and value:  # Collision happened
                if side == 'top':
                    player.place(player.pos.x, player.pos.y - value)
                if side == 'bottom':
                    player.place(player.pos.x, player.pos.y + value)
                if side == 'left':
                    player.place(player.pos.x - value, player.pos.y)
                if side == 'right':
                    player.place(player.pos.x + value, player.pos.y)
        if isinstance(entity, Portal):
            side, value = colliderect_info(entity.rect, player.rect)
            if side:  # Inside
                if side == 'inside':
                    player.portal = entity

    # Render entities
    for entity in sprite_groups[sprite_group_index]:
        entity.update()
        entity.blit()

    # Update display and clock
    pygame.display.update()
    clock.tick(fps)

pygame.quit()

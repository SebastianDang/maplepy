import sys
import pygame
from utils import colliderect_info
from config import Config
from player import Player
from world import Background, Obstacle

# Get configuration parameters
config = Config.instance()
config.init('etc/config.json')

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((config['width'], config['height']))
pygame.display.set_caption(config['caption'])
clock = pygame.time.Clock()
fps = config['fps']
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
    sprite_group.add(player)
    sprite_groups.append(sprite_group)

is_running = True
while is_running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.event.clear()
            is_running = False
            continue

    # Input key handling
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_TAB] and pygame.K_TAB not in key_delay:
        key_delay[pygame.K_TAB] = 60
        sprite_group_index = (sprite_group_index + 1) % len(sprite_groups)
    if pressed_keys[pygame.K_DOWN]:
        player.on_down()
    if not pressed_keys[pygame.K_DOWN]:
        player.off_down()
    if pressed_keys[pygame.K_LEFT]:
        player.on_left()
    if pressed_keys[pygame.K_RIGHT]:
        player.on_right()
    if pressed_keys[pygame.K_LALT]:
        player.on_jump()
    if pressed_keys[pygame.K_LCTRL]:
        player.on_attack()

    # Input Key handling for repeated characters
    key_delay_removal = []
    for key, delay in key_delay.items():
        key_delay[key] = delay - 1
        if key_delay[key] <= 0:
            key_delay_removal.append(key)
    for key in key_delay_removal:
        key_delay.pop(key, None)

    # Render black
    screen.fill((0, 0, 0))

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

    # Render entities
    for entity in sprite_groups[sprite_group_index]:
        entity.update()
        entity.blit()

    # Update display and clock
    pygame.display.update()
    clock.tick(fps)

pygame.quit()

import sys
import pygame
from utils import colliderect_info
from config import Config
from player import Player
from world import Background, Obstacle

config = Config.instance()
config.init('etc/config.json')

pygame.init()

screen = pygame.display.set_mode((config['width'], config['height']))
clock = pygame.time.Clock()
pygame.display.set_caption(config['caption'])
fps = config['fps']

background = Background(screen)

floor = Obstacle(screen)
floor.init(512, 533, 1024, 54)

left_wall = Obstacle(screen)
left_wall.init(0, config['height']/2, 1, config['height'])

right_wall = Obstacle(screen)
right_wall.init(config['width']-1, config['height']/2, 1, config['height'])

player = Player(screen)
player.place(512, 510)

all_sprites = pygame.sprite.Group()
all_sprites.add(background)
all_sprites.add(floor)
all_sprites.add(left_wall)
all_sprites.add(right_wall)
all_sprites.add(player)

while True:

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.event.clear()
            pygame.quit()
            sys.exit()

    # Input key handling
    pressed_keys = pygame.key.get_pressed()
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

    # Render black
    screen.fill((0, 0, 0))

    # Collision detection
    for entity in all_sprites:
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
    for entity in all_sprites:
        entity.update()
        entity.blit()

    # Update display and clock
    pygame.display.update()
    clock.tick(fps)

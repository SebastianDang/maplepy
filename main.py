import sys
import pygame
from config import Config
from player import Player
from world import Background, Platform

config = Config.instance()
config.init('etc/config.json')

pygame.init()

screen = pygame.display.set_mode((config['width'], config['height']))
clock = pygame.time.Clock()
pygame.display.set_caption(config['caption'])

background = Background(screen)
player = Player(screen)
player.place(512,510)

all_sprites = pygame.sprite.Group()
all_sprites.add(background)
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

    screen.fill((0, 0, 0))

    for entity in all_sprites:
        entity.update()
        entity.blit()

    pygame.display.update()
    clock.tick(config['fps'])

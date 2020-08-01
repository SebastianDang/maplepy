import sys
import pygame
from config import Config
from player import Player
from world import Platform

config = Config('etc/config.json')

pygame.init()
screen = pygame.display.set_mode((config['width'], config['height']))
clock = pygame.time.Clock()
pygame.display.set_caption(config['caption'])

platform = Platform(screen)
player = Player(screen)

all_sprites = pygame.sprite.Group()
all_sprites.add(platform)
all_sprites.add(player)

while True:

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Input key handling
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_LEFT]:
        player.left()
    if pressed_keys[pygame.K_RIGHT]:
        player.right()

    screen.fill((0, 0, 0))

    for entity in all_sprites:
        entity.update()
        entity.blit()

    pygame.display.update()
    clock.tick(config['fps'])

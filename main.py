import sys
import pygame
from config import Config
from player import Player
from world import Platform

config = Config('etc/config.json')

pygame.init()
displaysurface = pygame.display.set_mode((config['width'], config['height']))
clock = pygame.time.Clock()
pygame.display.set_caption(config['caption'])

platform = Platform()
player = Player()

all_sprites = pygame.sprite.Group()
all_sprites.add(platform)
all_sprites.add(player)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    displaysurface.fill((0, 0, 0))

    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)

    pygame.display.update()
    clock.tick(config['fps'])

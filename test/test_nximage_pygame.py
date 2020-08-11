import pygame
import os
from nx.nxfile import NXFile
from maplepy.nx.nxsprite import NXSprite
from maplepy.nx.nxspritemanager import NXSpriteManager

path = 'P:/Downloads/Resources'  # TODO: Change this to use your nx path


def test_nxsprite():

    node = NXFile(os.path.join(path, 'map.nx')).resolve(
        "Back/grassySoil.img/back/0")
    byte = node.getImage()

    assert node.name == '0'
    assert node.width == 256
    assert node.height == 256
    assert len(byte) == 256 * 256 * 4

    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    sprite = NXSprite()
    sprite.load(node.width, node.height, byte)
    sprite.image = pygame.transform.scale(sprite.image, screen.get_size())

    while(True):

        # Test event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.event.clear()
                pygame.quit()
                return
        pygame.event.pump()

        # Blit image as normal
        screen.blit(sprite.image, sprite.rect)

        # Update display
        pygame.display.update()


def test_nxsprite2():

    node = NXFile(os.path.join(path, 'map.nx')).resolve(
        "Tile/grassySoil.img/bsc/0")
    byte = node.getImage()

    assert node.name == '0'
    assert node.width == 90
    assert node.height == 60
    assert len(byte) == 90 * 60 * 4

    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    sprite = NXSprite()
    sprite.load(node.width, node.height, byte)
    sprite.image = pygame.transform.scale(sprite.image, screen.get_size())

    while(True):

        # Test event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.event.clear()
                pygame.quit()
                return
        pygame.event.pump()

        # Blit image as normal
        screen.blit(sprite.image, sprite.rect)

        # Update display
        pygame.display.update()


def test_nxspritemanager():

    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    file = NXFile(os.path.join(path, 'map.nx'))
    manager = NXSpriteManager()
    manager.file = file
    sprite = manager.get_sprite('Back', 'grassySoil', 'back', 'back/0')
    sprite2 = manager.get_sprite('Tile', 'grassySoil', None, 'bsc/0',)
    sprite3 = manager.get_sprite('Obj', 'acc1', 'grassySoil', 'nature/0/0')
    sprite.image = pygame.transform.scale(sprite.image, screen.get_size())
    sprite2.image = pygame.transform.scale(sprite2.image, screen.get_size())
    sprite3.image = pygame.transform.scale(sprite3.image, screen.get_size())

    while(True):

        # Test event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.event.clear()
                pygame.quit()
                return
        pygame.event.pump()

        # Blit image as normal
        screen.blit(sprite.image, sprite.rect)
        screen.blit(sprite2.image, sprite2.rect)
        screen.blit(sprite3.image, sprite3.rect)

        # Update display
        pygame.display.update()

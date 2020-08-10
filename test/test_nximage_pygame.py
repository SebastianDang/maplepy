import pygame
import os
from nx.nxfile import NXFile
from maplepy.nx.nxsprite import NXSprite

path = 'P:/Downloads/Resources'  # TODO: Change this to use your nx path


def test_nximage_pygame():

    # node = NXFile("map.nx").getRoot().getChild("Tile").getChild(
    #     'grassySoil.img').getChild('bsc').getChild('0')
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

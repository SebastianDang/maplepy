from nxfile import NXFile
import pygame
from nxsprite import nxsprite


# tile = NXFile("map.nx").getRoot().getChild("Tile").getChild(
#     'grassySoil.img').getChild('bsc').getChild('0')

tile = NXFile("map.nx").resolve("Tile/grassySoil.img/bsc/0")
print(tile)
print(tile.name)
print('height', tile.height)
print('width', tile.width)
print('size', tile.width * tile.height)
print(tile.childCount)
print(tile.populateChildren())
byte = tile.getImage()


pygame.init()
screen = pygame.display.set_mode((800, 600))

sprite = nxsprite()
sprite.load(tile.width, tile.height, byte)
sprite.image = pygame.transform.scale(sprite.image, screen.get_size())

while(True):

    # Test event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.event.clear()
            pygame.quit()
            exit()
    pygame.event.pump()

    # Blit image as normal
    screen.blit(sprite.image, sprite.rect)

    pygame.display.update()

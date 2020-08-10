import numpy
import io
import PIL.Image as Image
import math
from nxfile import NXFile
import pygame

# bgra
# rgb


def convertRawBytesToArray(bytes):
    res = []
    for i in range(math.floor(len(bytes) / 4)):
        # print(i)
        res.append(tuple([bytes[i+2], bytes[i + 1], bytes[i], bytes[i+3]]))
    return res


tile = NXFile("map.nx").getRoot().getChild("Tile").getChild(
    'grassySoil.img').getChild('bsc').getChild('0')
print(tile)
print(tile.name)
print('height', tile.height)
print('width', tile.width)
print('size', tile.width * tile.height)
print(tile.childCount)
print(tile.populateChildren())
byte = tile.getImage()
# print(byte)
data = convertRawBytesToArray(byte)

pygame.init()
screen = pygame.display.set_mode((800, 600))

# Image properties
w = tile.width
h = tile.height
# data = [(255, 0, 0, 255), (255, 0, 0, 255), (0, 255, 0, 255), (0, 255, 0, 255)]

# Create an image (surface) with target width and height
image = pygame.Surface((w, h))

# Access the surface as a pixel array
pxarray = pygame.PixelArray(image)
for y in range(0, h):
    for x in range(0, w):
        pxarray[x, y] = data[y * w + x]
# pixel array must be deleted to 'unlock' the image
del pxarray
# Call unlock, to be safe
image.unlock()

# Scale so you can view it!!
image = pygame.transform.scale(image, screen.get_size())

while(True):

    # Test event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.event.clear()
            pygame.quit()
            exit()
    pygame.event.pump()

    # Blit image as normal
    screen.blit(image, image.get_rect())

    pygame.display.update()

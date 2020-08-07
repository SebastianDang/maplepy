import time
import pygame
from Wz.Map.Map_sprites import Map_sprites

pygame.init()
w, h = 2000, 800
screen = pygame.display.set_mode((w, h))

# Timer start
t0 = time.time()
print('Loading.')

# Load
m = Map_sprites(screen)
m.path = 'P:\Downloads\MapleStory'
m.load_map('000010000')  # 100000000
m.load_info()
m.load_back_sprites()
m.load_tile_sprites()
m.load_object_sprites()

# Timer stop
t1 = time.time()
total = t1-t0
print('Loading took', "{0:0.2f}".format(total), 'seconds.')

while(True):
    # Events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.event.clear()
            pygame.quit()
            exit()
    pygame.event.pump()
    # Camera movement test
    speed = 10
    inputs = pygame.key.get_pressed()
    if inputs[pygame.K_UP]:
        m.cam = m.cam.move(0, -speed)
    if inputs[pygame.K_DOWN]:
        m.cam = m.cam.move(0, speed)
    if inputs[pygame.K_LEFT]:
        m.cam = m.cam.move(-speed, 0)
    if inputs[pygame.K_RIGHT]:
        m.cam = m.cam.move(speed, 0)
    if inputs[pygame.K_r]:
        m.cam.update(0, 0)

    # Draw
    screen.fill((0, 0, 0))
    m.update()
    m.blit()
    pygame.display.update()

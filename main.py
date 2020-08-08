import time
import pygame
from wz.map.MapDisplay import MapDisplay

w, h = 1920, 1080
fps = 60

pygame.init()
screen = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()

# Timer start
t0 = time.time()
print('Loading.')

# Load
m = MapDisplay(screen)
m.path = 'P:\Downloads\MapleStory'
m.load_map('000010000')  # Maple Tree Hill
# m.load_map('100000000')  # Henesys

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
    clock.tick(fps)

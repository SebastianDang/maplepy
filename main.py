import pygame
from game import *


# Get configuration parameters
config = Config.instance()
config.init('etc/config.json')

# Init pygame
pygame.init()

# Create game
game = Game()
game.init()
game.load_player()
game.load_map(1)
game.running = True

# Game running loop
while(game.running):
    game.update()
    game.draw()

# Quit pygame
pygame.quit()

import pygame
from game import *


# Get configuration parameters
config = Config.instance()
config.init('etc/config.json')

# Init pygame
pygame.init()

# Set icon
icon = pygame.image.load(config['icon'])
pygame.display.set_icon(icon)

# Create game
game = Game()
game.init()
game.load_player()
game.load_map(0)
game.running = True

# Game running loop
while(game.running):
    game.update()
    game.draw()

# Quit pygame
pygame.quit()

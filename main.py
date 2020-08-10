# Add nx to system path
import sys
sys.path.insert(0, './nx')

# Import maplepy
from maplepy.game.game import Game

# Run
game = Game('config.json')
game.run()

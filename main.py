import sys
import logging
from maplepy.game.game import Game

# Add nx to system path
sys.path.insert(0, './nx')

# Set up logging module
logging.basicConfig(format='%(asctime)s %(levelname)s %(module)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.WARNING)

# Run
game = Game('config.json')
game.run()

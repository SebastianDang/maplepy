import logging

from maplepy.game.game import Game

# Set up logging module
logging.basicConfig(format='%(asctime)s %(levelname)s %(module)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

# Run
game = Game('config.json')
game.run()

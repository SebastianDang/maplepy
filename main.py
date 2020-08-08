from wz.game.Game import Game

w, h = 1920, 1080
game = Game(w,h)
game.set_path('P:\Downloads\MapleStory')
game.load()
game.run()

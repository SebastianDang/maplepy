import os
import pygame


class Sound_Bgm:
    def __init__(self):
        self.file = None
        self.volume = 1.0
        self.loop = -1

    def play_bgm(self, path, bgm):
        if bgm:
            file = "{}/{}.mp3".format(path, bgm)
            if os.path.isfile(file):
                pygame.mixer.init()
                pygame.mixer.music.load(file)
                pygame.mixer.music.set_volume(self.volume)
                pygame.mixer.music.play(self.loop)
                self.file = file

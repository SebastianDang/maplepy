import os

import pygame


class Bgm:
    """ Class to handle sounds from a file or from a buffer """

    def __init__(self):
        self.name = None
        self.file = None
        self.sound = None
        self.channel = None

    def load(self, name, file=None, buffer=None):
        try:

            # Check arguments
            if self.name == name:
                return

            # Unload previous
            if self.file:
                pygame.mixer.music.stop()

            if self.sound:
                self.sound.stop()

            # Load from file
            if file and os.path.isfile(file):
                pygame.mixer.music.load(file)
                self.file = file

            # Load from buffer
            if buffer:
                self.sound = pygame.mixer.Sound(buffer=buffer)

            # Update name
            self.name = name

        except:
            pass

    def volume(self, val):

        if self.file:
            pygame.mixer.music.set_volume(val)

        if self.sound:
            self.sound.set_volume(val)

    def play(self):

        if self.channel and self.channel.get_busy():
            return

        if self.file:
            self.channel = pygame.mixer.music.play(loops=-1, fade_ms=250)

        if self.sound:
            self.channel = self.sound.play(loops=-1, fade_ms=250)

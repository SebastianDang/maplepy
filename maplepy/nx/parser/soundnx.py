import logging
import os

from libnx.nxfile import NXFileSet


class SoundNx:
    """ Helper class to get values from a sound nx file. """

    def __init__(self):
        self.file = NXFileSet()

    def open(self, file):
        """ Load file from path """

        # Check if file exists
        if not os.path.exists(file):
            logging.warning(f'{file} does not exist')
            return
        try:
            # Open nx file
            self.file.load(file)
        except:
            logging.exception(f'Unable to open {file}')

    def get_sound(self, path):
        """
        Get audio buffer from byte array
        Convert audio to wav stream pcm_s16le: PCM signed 16-bit little-endian
        Target sample rate is 44100hz
        """

        # Get sound node
        paths = path.split('/')
        sound_path = f'{paths[0]}.img/{paths[1]}'
        sound_node = self.file.resolve(sound_path)
        if not sound_node:
            return None

        # Get sound data
        sound = sound_node.get_sound()
        return sound.get_data()

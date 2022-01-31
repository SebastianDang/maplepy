import io
import logging
import os

from libnx.nxfile import NXFileSet
from pydub import AudioSegment


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
        data = io.BytesIO(sound[82:])

        # header = sound[32:82]
        # fmt = int.from_bytes(header[8:12], 'big')
        # channels = int.from_bytes(header[22:24], 'little')
        # sample_rate = int.from_bytes(header[24:28], 'little')
        # byte_rate = int.from_bytes(header[28:32], 'little')
        # block_align = int.from_bytes(header[32:34], 'little')
        # bits_per_sample = int.from_bytes(header[34:36], 'little')

        # Convert to wav
        audio_bytes = io.BytesIO()
        audio = AudioSegment.from_file(data)
        audio.export(audio_bytes,
                     format='wav',
                     codec='pcm_s16le',
                     parameters=['-ar', '44100'])
        return audio_bytes.getbuffer()

import os
import io
import nx.nxfile as nxfile
from nx.nxfileset import NXFileSet
from pydub import AudioSegment


class SoundNx:
    def __init__(self):
        self.file = NXFileSet()

    def open(self, file):
        # Check if file exists
        if not os.path.exists(file):
            print('{} does not exist'.format(file))
            return
        try:
            # Open nx file
            self.file.load(file)
        except:
            print('Unable to open {}'.format(file))

    def get_sound(self, path):
        paths = path.split('/')
        soundPath = '{}.img/{}'.format(paths[0], paths[1])
        sound_node = self.file.resolve(soundPath)
        if not sound_node:
            return None

        # Get sound data
        sound = sound_node.getSound()

        # Debug audio format
        # for i in range(0, 50):
        #     header = sound[i:82]
        #     fmt = header[8:12]
        #     channels = header[22:24]
        #     sample_rate = header[24:28]
        #     byte_rate = header[28:32]
        #     block_align = header[32:34]
        #     bits_per_sample = header[34:36]

        #     fmt = int.from_bytes(fmt, 'big')
        #     channels = int.from_bytes(channels, 'little')
        #     sample_rate = int.from_bytes(sample_rate, 'little')
        #     byte_rate = int.from_bytes(byte_rate, 'little')
        #     block_align = int.from_bytes(block_align, 'little')
        #     bits_per_sample = int.from_bytes(bits_per_sample, 'little')

        #     pass

        # Read header
        header = sound[32:82]
        channels = int.from_bytes(header[22:24], 'little')
        sample_rate = int.from_bytes(header[24:28], 'little')

        # Update codec
        codec = None
        if sample_rate == 22050:
            codec = 'pcm_s32le'
        elif sample_rate == 44100:
            codec = 'pcm_s16le'

        # Get data
        data = io.BytesIO(sound[82:])

        # Convert to wav
        audio_bytes = io.BytesIO()
        audio = AudioSegment.from_file(data)
        audio.export(audio_bytes, format='wav', codec=codec)
        return audio_bytes.getbuffer()

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
        data = io.BytesIO(sound[82:])

        # # Debug audio format
        # for i in range(0, 50): # 32

        #     header = sound[i:82]

        #     fmt = int.from_bytes(header[8:12], 'big')
        #     channels = int.from_bytes(header[22:24], 'little')
        #     sample_rate = int.from_bytes(header[24:28], 'little')
        #     byte_rate = int.from_bytes(header[28:32], 'little')
        #     block_align = int.from_bytes(header[32:34], 'little')
        #     bits_per_sample = int.from_bytes(header[34:36], 'little')

        #     pass

        # Convert to wav
        audio_bytes = io.BytesIO()
        audio = AudioSegment.from_file(data)
        audio.export(audio_bytes,
                     format='wav',
                     codec='pcm_s16le',
                     parameters=['-ar', '44100'])
        return audio_bytes.getbuffer()

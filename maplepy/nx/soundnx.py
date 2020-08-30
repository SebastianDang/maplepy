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

        sound_bytes = io.BytesIO(sound_node.getSound()[:])
        audio_bytes = io.BytesIO()
        audio = AudioSegment.from_file(sound_bytes)
        audio.export(audio_bytes, format='wav')
        return audio_bytes.getbuffer()

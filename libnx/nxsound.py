import io

from pydub import AudioSegment


def unpack_data_to_wav(data):

    # header = sound[32:82]
    # fmt = int.from_bytes(header[8:12], 'big')
    # channels = int.from_bytes(header[22:24], 'little')
    # sample_rate = int.from_bytes(header[24:28], 'little')
    # byte_rate = int.from_bytes(header[28:32], 'little')
    # block_align = int.from_bytes(header[32:34], 'little')
    # bits_per_sample = int.from_bytes(header[34:36], 'little')

    data_bytes = io.BytesIO(data[82:])

    # Convert to wav
    audio_bytes = io.BytesIO()
    audio = AudioSegment.from_file(data_bytes)
    audio.export(audio_bytes,
                    format='wav',
                    codec='pcm_s16le',
                    parameters=['-ar', '44100'])
    return audio_bytes.getbuffer()


class NXSound:

    def __init__(self, nxfile, offset, length):
        self.nxfile = nxfile
        self.offset = offset
        self.length = length

    def get_data(self):
        """ Get sound data """
        self.nxfile.file.seek(self.offset)
        data = self.nxfile.file.read(self.length)
        return unpack_data_to_wav(data)

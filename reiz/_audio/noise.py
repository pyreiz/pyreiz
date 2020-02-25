from pyglet.media.synthesis import SynthesisSource, WhiteNoise
import ctypes
import random
from reiz._audio.fft import transform


class BrownNoise(SynthesisSource):
    """A waveform. of brown noise, i.e. with 1/f² 
    :Parameters:
        `duration` : float
            The length, in seconds, of audio that you wish to generate.
        `sample_rate` : int
            Audio samples per second. (CD quality is 44100).
    """

    def __init__(self, duration, **kwargs):
        super().__init__(duration, **kwargs)
        
    def _generate_data(self, num_bytes):
        samples = num_bytes >> 1
        amplitude = 32767
        fxx  = []
        for i in range(samples):
            tmp = random.normalvariate(0, 1) + 1j * random.normalvariate(0, 1) 
            fxx.append(tmp / (i+1))
        data = (ctypes.c_short * samples)()
        envelope = self._envelope_generator
        signal = transform(fxx, inverse=True)
        for i in range(samples):
            data[i] = int(signal[i].real  * amplitude * next(envelope))
        return data
# -*- coding: utf-8 -*-
"""Building blocks for auditory stimuli
"""

from .tts import PlatformIndependentMessage as Message
from sys import platform
from threading import Timer
import time
from pyglet.media.codecs.base import StaticSource
from pyglet.media.synthesis import ADSREnvelope, Sine
import pyglet

# %%


class Sound():
    """interface for a generic sound object"""
    source = None

    def play(self):
        """start playing the sound and return immediatly

        returns
        -------
        remainder: float
            seconds until the sound would be finished playing
        """
        t0 = time.time()
        player = self.source.play()
        t = Timer(player.source.duration, player.delete)
        t.start()
        return player.source.duration + t0 - time.time()

    def play_blocking(self) -> float:
        """"play the sound and block until playing is finished

        returns
        -------
        remainder: float
            seconds until the sound would finish playing. Naturally, it always
            returns 0. The output is kept here to allow easy substitution with
            : func: `Sound.play`
        """
        rest = self.play()
        t0 = time.time()
        while (time.time()-t0) < rest:
            pass
        return 0

    @property
    def duration(self) -> float:
        "returns duration of the sound in seconds"
        return self.source.duration

    def __repr__(self):
        return str(self.source)


class AnySource(Sound):
    """
    args
    ----
    source: StaticSource
        the source of the sound. Usually you instantiate one of the
        inheriting objects, e.g. :class:`~.AudioFile` or :class`~.Hertz`
        which allow more parameters.

    """

    def __init__(self, source: StaticSource = None):
        self.source = source


class Hertz(Sound):
    """instantiate a sine wave with ramp-up and ramp-down period of volume

    args
    ----
    duration_in_ms: float
        duration of the sound in ms
    frequency: int
        frequency in Hz
    volume: float
        relative volume
    """

    def __init__(self, duration_in_ms: float = 500, frequency: int = 440, volume: float = 1):

        adsr = ADSREnvelope(attack=duration_in_ms/8000,
                            decay=duration_in_ms/2000,
                            release=duration_in_ms/8000,
                            sustain_amplitude=volume)
        sine = Sine(duration=duration_in_ms/1000, frequency=frequency,
                    sample_size=16, sample_rate=44100, envelope=adsr)
        self.source = pyglet.media.StaticSource(sine)


class AudioFile(Sound):
    """instantiate a sound object from a wav-file

    args
    ----
    filepath: str
        path to the wav-file
    """

    def __init__(self, filepath: str):
        self.source = pyglet.media.load(filepath, streaming=False)


# # Text-to-speech depends on the platform
# if platform == "linux":
#     from .tts import Espeak_Mixin

#     class Message(Espeak_Mixin, Sound):
#         pass

# elif platform == 'win32':
#     from .tts import PlatformIndependentMessage as Message
# else:
#     from .tts import gTTS_Mixin

#     class Message(gTTS_Mixin, Sound):
#         pass

# -*- coding: utf-8 -*-
"""
Building blocks for auditory stimuli
....................................
"""

from .tts import tts_Mixin
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
    volume = 1

    def play(self):
        """start playing the sound and return immediatly

        returns
        -------
        remainder: float
            seconds until the sound would be finished playing
        """
        t0 = time.time()
        player = self.source.play()
        player.volume = self.volume
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
        self._duration_in_ms = duration_in_ms
        self._frequency = frequency
        self.source = pyglet.media.StaticSource(sine)
        self.volume = volume

    def __repr__(self):
        return f"Hertz(duration_in_ms={self._duration_in_ms}, frequency= {self._frequency})"


class AudioFile(Sound):
    """instantiate a sound object from a wav-file

    args
    ----
    filepath: str
        path to the wav-file
    """

    def __init__(self, filepath: str):
        self.source = pyglet.media.load(filepath, streaming=False)


class Message(tts_Mixin, Sound):
    """Text-to-Speech Audio Stimulus

    If reiz was installed with `[tts]` as extra, this class will use pyttsx3
    to generate auditory stimuli on demand. If pyttsx3 is not found, there will be only silence when creating an `audio.Message`.
    """
    pass

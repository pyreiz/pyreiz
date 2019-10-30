# -*- coding: utf-8 -*-
"""
Auditory stimuli
"""

import pyglet
from pyglet.media.synthesis import ADSREnvelope, Sine
import time
from threading import Timer
# pyglet.options['audio'] = ('openal', 'pulse', 'directsound', 'silent')
# %%


class Sound():

    def play(self):
        t0 = time.time()
        player = self.sound.play()
        t = Timer(player.source.duration, player.delete)
        t.start()
        return player.source.duration + t0 - time.time()

    def play_blocking(self):
        rest = self.play(self.sound)
        t0 = time.time()
        while (time.time()-t0) < rest:
            pass
        return 0

    def queue(self, speaker):
        speaker.queue(self.sound)

    @property
    def duration(self):
        return self.sound.duration

    def __repr__(self):
        # self.play()
        return str(self.sound)


class Hertz(Sound):
    def __init__(self, duration_in_ms: float = 500, frequency: int = 440, volume=1):
        'creates a sine wave with ramp-up and ramp-down period of volume'
        adsr = ADSREnvelope(attack=duration_in_ms/8000,
                            decay=duration_in_ms/2000,
                            release=duration_in_ms/8000,
                            sustain_amplitude=volume)
        sine = Sine(duration=duration_in_ms/1000, frequency=frequency,
                    sample_size=16, sample_rate=44100, envelope=adsr)
        self.sound = pyglet.media.StaticSource(sine)


class AudioFile(Sound):

    def __init__(self, filepath: str):
        self.sound = pyglet.media.load(filepath, streaming=False)

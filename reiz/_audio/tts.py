# -*- coding: utf-8 -*-
"""
Created on Mon May 20 10:50:52 2019

@author: Robert Guggenberger
"""
from tempfile import NamedTemporaryFile
from subprocess import run
from typing import Callable
from threading import Thread
import time
import pyglet.media
from sys import platform
import importlib


class PlatformIndependentMessage():
    """instantiate a tts sound object

    args
    ----
    message: str
        the content of the message, e.g. "Hello World"
    voiceid:int
        the id of the voice
    rate:int
        the speed of the Utterance
    """

    def __init__(self, message: str = "Hello World",
                 rate=135, voiceid=0):
        if "darwin" in platform:
            self.engine = pyttsx3.init("dummy")
        else:
            self.engine = pyttsx3.init()
        self.engine.setProperty('rate', rate)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[voiceid])
        self.message = message
        self._duration = self._estimate_duration()

    def _estimate_duration(self):
        t0 = time.time()
        self.engine.setProperty('volume', 0.)
        self.play_blocking()
        t1 = time.time()
        self.engine.setProperty('volume', 1.)
        return t1-t0

    @property
    def volume(self):
        return self.engine.getProperty('volume')

    @volume.setter
    def volume(self, volume: float):
        self.engine.setProperty('volume', volume)

    def play_blocking(self):
        """
        returns
        -------
        remainder:float
            seconds until the sound would finish playing. Naturally, it always
            returns 0. The output is kept here to allow easy substitution with
            :func:`Sound.play`
        """
        self.engine.say(self.message)
        self.engine.runAndWait()
        return 0

    def stop(self):
        self.engine.stop()

    def play(self):
        """start playing the sound and return immediatly

        returns
        -------
        remainder:float
            seconds until the sound would be finished playing
        """
        t0 = time.time()
        t = Thread(target=self.play_blocking)
        t.start()
        return self.duration + t0 - time.time()

    @property
    def duration(self) -> float:
        "returns duration of the sound in seconds"
        return self._duration

    def __repr__(self):
        return f"{self.__class__} {str(self.message)}"


class Espeak_Mixin(object):

    def __init__(self, message: str = "Espeak says",
                 rate: int = 135,
                 gender="f",
                 language="de"):
        self.message = message
        if gender.lower() not in ["m", "f"]:
            raise ValueError("Gender must be (m)ale or (f)emale")

        with NamedTemporaryFile(suffix=".wav") as f:
            run(["espeak", f"\"{message}\""
                 "-s", str(rate),
                 f"-v{language.lower()}+{gender.lower()}1",
                 # increase  pitch for words which begin a capital letter.
                 "-k10",
                 "-g2",
                 "-w", f.name])
            self.source = pyglet.media.load(f.name, streaming=False)


class Silent_Mixin(object):
    def __init__(self, message: str = "Silence is golden",
                 language="de"):
        self.message = message
        print("no TTS is installed on your system. Default to silence")
        from pyglet.media.synthesis import Silence
        self.source = Silence(duration=0.1)
        return


# class gTTS_Mixin():

#     def __init__(self, message: str = "Google says",
#                  language="de"):
#         self.message = message
#         try:
#             from gtts import gTTS
#         except ImportError:
#             print("gTTS is not installed on your system. Default to silence")
#             from pyglet.media.synthesis import Silence
#             self.source = Silence(duration=0.1)
#             return

#         with NamedTemporaryFile(suffix=".wav") as f:
#             tts = gTTS(message, lang=language)
#             tts.save(f.name)
#             run(["ffmpeg", "-i", f.name, f.name, "-y"])
#             self.source = pyglet.media.load(f.name, streaming=False)


# conditional interface for Message

if importlib.util.find_spec("pyttsx3") is None:  # pragma: no cover
    tts_Mixin = Silent_Mixin
else:
    if "darwin" in platform:  # pragma: no cover
        tts_Mixin = Silent_Mixin
    else:
        import pyttsx3
        tts_Mixin = PlatformIndependentMessage

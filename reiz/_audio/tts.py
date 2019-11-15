# -*- coding: utf-8 -*-
"""
Created on Mon May 20 10:50:52 2019

@author: Robert Guggenberger
"""

# %%
import pyttsx3
from typing import Callable
from threading import Thread
import time
import pyglet.media


class Espeak_Mixin(object):

    def __init__(self, message: str = "Hallo Welt und Goodbye",
                 rate: int = 135,
                 gender="f",
                 language="de"):
        self.message = message
        if gender.lower() not in ["m", "f"]:
            raise ValueError("Gender must be (m)ale or (f)emale")

        from subprocess import run
        from tempfile import NamedTemporaryFile
        with NamedTemporaryFile(suffix=".wav") as f:
            run(["espeak", f"\"{message}\""
                 "-s", str(rate),
                 f"-v{language.lower()}+{gender.lower()}1",
                 # increase  pitch for words which begin a capital letter.
                 "-k10",
                 "-g2",
                 "-w", f.name])
            self.source = pyglet.media.load(f.name, streaming=False)


class PlatformIndependentMessage():
    """instantiate a generic sound object

    args
    ----
    message: str
        the content of the message, e.g. "Hello World"

    """

    def __init__(self, message: str = "Hello World",
                 rate=135, voiceid=0):
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

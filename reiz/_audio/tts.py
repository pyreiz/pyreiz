# -*- coding: utf-8 -*-
"""
Created on Mon May 20 10:50:52 2019

@author: Robert Guggenberger
"""
from tempfile import TemporaryDirectory
from subprocess import run
from sys import platform
import importlib
from time import sleep

try:
    import pyttsx3
    from pathlib import Path

    if "darwin" in platform:
        engine = pyttsx3.init("dummy")
    else:
        engine = pyttsx3.init()
    tmpdir = TemporaryDirectory(suffix="tts", dir="./")
except ImportError:
    print("pyttsx3 not found")
    pyttsx3 = None

import pyglet.media


class PlatformIndependentMessage:
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

    def __init__(self, message: str = "Hello World", rate=135, voiceid=0):
        engine.setProperty("rate", rate)
        voices = engine.getProperty("voices")
        engine.setProperty("voice", voices[voiceid])
        self.message = message
        f = (Path(f"{tmpdir.name}") / Path(f"{message}.mp3")).resolve()
        engine.save_to_file(message, str(f))
        engine.runAndWait()
        while not f.exists():
            sleep(0.1)
            print(".", end="")
        print(f"Created temporary audiofile at {f}")
        self.source = pyglet.media.load(str(f), streaming=False)

    def __repr__(self):
        return f"{self.__class__.__name__} {str(self.message)}"


class Espeak_Mixin(object):
    def __init__(
        self,
        message: str = "Espeak says",
        rate: int = 135,
        gender="f",
        language="de",
    ):
        self.message = message
        if gender.lower() not in ["m", "f"]:
            raise ValueError("Gender must be (m)ale or (f)emale")

        with NamedTemporaryFile(suffix=".wav") as f:
            run(
                [
                    "espeak",
                    f'"{message}"' "-s",
                    str(rate),
                    f"-v{language.lower()}+{gender.lower()}1",
                    # increase  pitch for words which begin a capital letter.
                    "-k10",
                    "-g2",
                    "-w",
                    f.name,
                ]
            )
            self.source = pyglet.media.load(f.name, streaming=False)

    def __repr__(self):
        return f"{self.__class__.__name__} {str(self.message)}"


class Silent_Mixin(object):
    def __init__(self, message: str = "Silence is golden", language="de"):
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

"""
API to auditory stimuli
"""
from os import environ as _env
from reiz._audio.primitives import AudioFile, Hertz, Message
from pathlib import Path
from typing import Dict
from types import SimpleNamespace

_defaults = {"Message":
             {"start": {"message": "start"}},
             "Hertz":
             {"beep": {"duration_in_ms": 1000}},
             }


def make_library(settings: Dict = _defaults) -> SimpleNamespace:
    lib = dict()
    for key in settings.keys():
        for name, args in settings[key].items():
            if key.lower() == "audiofile":
                lib[name] = AudioFile(**args)
            elif key.lower() == "message":
                lib[name] = Message(**args)
            elif key.lower() == "hertz":
                lib[name] = Hertz(**args)
    lib = SimpleNamespace(**lib)
    return lib


def read_folder(path: Path = None) -> SimpleNamespace:
    'create an audio library from path'
    if path is None or not path.exists():
        raise ValueError(f"{path} not found")
    library = dict()
    import os
    for f in os.listdir(path):
        key = os.path.splitext(f)[0]
        key = key.replace("(", "")
        key = key.replace(")", "")
        key = key.replace(" ", "_")
        key = key.replace("-", "_")
        key = key.strip()
        val = AudioFile(os.path.join(path, f))
        library[key] = val
    library = SimpleNamespace(**library)
    return library


library = make_library(_defaults)

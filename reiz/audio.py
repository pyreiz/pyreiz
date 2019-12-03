"""Creating and managing auditory stimuli
"""
from types import SimpleNamespace
from os import environ as _env
from reiz._audio.primitives import AudioFile, Hertz, Message
from pathlib import Path
from typing import Dict, NewType, Any
libConf = NewType("libConf", Dict[str, Dict[str, Any]]
                  )  #: Dict[str, Dict[str, Any], a dictionary of types and respective keywords arguments

_defaults = libConf({
    "Message": {
        "start": {"message": "start"}
    },
    "Hertz": {
        "beep": {"duration_in_ms": 1000}
    },
})  #: libConf


def make_library(settings: libConf = _defaults, failraise=False) -> SimpleNamespace:
    """create a library of auditory stimuli from a dictionary of arguments

    args
    ----
    settings:
        a dictionary of types with kwargs appropriate to the respective type
        as dictionary
    failraise:bool
        raise an exception if a key is not recognized. defaults to False

    returns
    -------

    library:
        a library of instances of stimuli which can be adressed in dot.notation
    """
    lib = dict()
    for key in settings.keys():
        for name, args in settings[key].items():
            if key.lower() == "audiofile":
                lib[name] = AudioFile(**args)
            elif key.lower() == "message":
                lib[name] = Message(**args)
            elif key.lower() == "hertz":
                lib[name] = Hertz(**args)
            else:
                if failraise:
                    raise ValueError(f"{key} with {args} can't be processed")
    lib = SimpleNamespace(**lib)
    return lib


def read_folder(path: Path = None) -> SimpleNamespace:
    'create an audio library from path'
    path = Path(path)
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


if not 'DOC' in _env.keys():
    library = make_library()
else:  # pragma: no cover
    mock = dict()
    for t, item in _defaults.items():
        for k, v in item.items():
            mock[k] = t
    library = SimpleNamespace(**mock)  #: a library of auditory stimuli
    print("Generating sphinx documentation. Skipping visual library")


__doc__ += f"""
During import, a basic library will be created. By default, it contains
the following set of auditory stimuli: {', '.join([str(k) for k in library.__dict__])}. These stimuli can be addressed by dot.notation from :data:`reiz.audio.library`, for example like :data:`reiz.audio.library.beep`


.. automodule:: reiz._audio.primitives
   :members: Message, Hertz, AudioFile

Create libraries of auditory stimuli
....................................

"""

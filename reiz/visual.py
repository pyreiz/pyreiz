"""Creating and managing visual stimuli
"""
import os
from os import environ as _env
from reiz._visual.complex import Mural, Image, Cross, Circle, Background, Line, Bar
from reiz._visual.complex import Polygon, Trapezoid, Cylinder
from reiz._visual.colors import COLORS, get_color
from types import SimpleNamespace
from typing import Dict, NewType, Any
from pathlib import Path
from pkg_resources import resource_filename

libConf = NewType("libConf", Dict[str, Dict[str, Any]]
                  )  #: Dict[str, Dict[str, Any], a dictionary of types and respective keywords arguments

_defaults = libConf({
    "Mural": {
        "post": {"text": "Run endet"},
        "pre": {"text": "Run beginnt"},
        "eo": {"text": "Augen offen"},
        "ec": {"text": "Augen zu"},
        "ready": {"text": "Bereit machen"},
        "los": {"text": "Los"},
        "go": {"text": "Go!"},
        "imagine": {"text": "Bewegung vorstellen"},
        "move": {"text": "Bewegung starten"},
        "count": {"text": "Zahlen berechnen"},
        "relax": {"text": "Entspannen"},
        "rating": {"text": "0 - 1 - 2 - 3 - 4 - 5 - 6 - 7 - 8 - 9 - 10", "fontsize": 0.75},
    },
    "Cross": {
        "fixation": {"color": "white"},
    },

    "Image": {
        "logo": {"imgpath": resource_filename(__name__, 'data/logo.png')},
    }

})  #: libConf


def make_library(settings: libConf = None, failraise=False) -> SimpleNamespace:
    """create a library of visual stimuli from a dictionary of arguments

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

    if settings is None:
        settings = _defaults
    library = dict()
    for key in settings.keys():
        for name, args in settings[key].items():
            if key.lower() == "mural":
                library[name] = Mural(**args)
            elif key.lower() == "cross":
                library[name] = Cross(**args)
            elif key.lower() == "image":
                library[name] = Image(**args)
            else:
                if failraise:
                    raise(f"{key} with {args} can't be processed")

    library = SimpleNamespace(**library)
    return library


if not 'DOC' in _env.keys():
    library = make_library()
else:   # pragma: no cover
    mock = dict()
    for t, item in _defaults.items():
        for k, v in item.items():
            mock[k] = t
    library = SimpleNamespace(**mock)  #: a library of visual stimuli
    print("Generating sphinx documentation. Skipping visual library")


__doc__ += f"""
During import, a basic library will be created. By default, it contains
the following set of visual stimuli: {', '.join([str(k) for k in library.__dict__])}. These stimuli can be addressed by dot.notation from :data:`reiz.visual.library`, for example like :data:`reiz.visual.library.go`

.. automodule:: reiz._visual.complex
   :members: Mural, Image, Cross, Circle, Background, Line, Bar, Polygon, Trapezoid, Cylinder

.. automodule:: reiz._visual.colors
   :members: COLORS, get_color

Create libraries of visual stimuli
..................................



"""

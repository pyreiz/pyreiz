import os
from os import environ as _env
from reiz._visual.complex import Mural, Image, Cross, Circle, Background, Line, Bar
from reiz._visual.complex import Polygon, Trapezoid, Cylinder
from types import SimpleNamespace
from typing import Dict
from pathlib import Path
from pkg_resources import resource_filename
_defaults = {
    "Murals": {
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

}


def make_library(settings: Dict = _defaults) -> SimpleNamespace:
    'create a library of visual stimuli from a dict'
    library = dict()
    for key in settings.keys():
        for name, args in settings[key].items():
            if key.lower() == "murals":
                library[name] = Mural(**args)
            elif key.lower() == "cross":
                library[name] = Cross(**args)
            elif key.lower() == "image":
                library[name] = Image(**args)
            else:
                raise ValueError(f"{key} with {args} can't be processed")

    library = SimpleNamespace(**library)
    return library


library = make_library()

import os
from os import environ as _env
from reiz._visual.complex import Mural, Image, Cross, Circle, Background, Line, Bar
from reiz._visual.complex import Polygon, Trapezoid, Cylinder
from types import SimpleNamespace
from typing import Dict
from pathlib import Path
rootfolder = Path(__file__).absolute().parent.parent
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
        "logo": {"imgpath": rootfolder / "media" / "logo.png"},
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
    print(library)
    library = SimpleNamespace(**library)
    return library


def read_settings(path: Path = None) -> Dict:
    'create settings-dict for library of visual stimuli from an ini-file'
    import configparser
    import json

    if path is None or not path.exists():
        raise ValueError(f"{path} not found")

    ini = configparser.ConfigParser()
    ini.read(os.path.join(path, f))
    d = dict()
    for s in ini.sections():
        d[s] = dict()
        for k, v in ini.items(s):
            try:
                d[s][k] = int(v)
                continue
            except ValueError:
                pass
            try:
                d[s][k] = json.loads(v)
                continue
            except json.JSONDecodeError:
                pass
            try:
                d[s][k] = str2list(v)
                continue
            except Exception as e:
                raise e

        return d

    return d


library = make_library()

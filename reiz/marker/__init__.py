from reiz.marker.soft import SoftMarker as _SoftMarker
_soft = _SoftMarker()

from os import environ as _env 
if not 'pyreiz-doc' in _env.keys():
    _soft.start()

def push(markerstr:str):
    _soft.push(markerstr)


from reiz.marker.soft import SoftMarker as _SoftMarker
_soft = _SoftMarker()

from os import environ as _env 
if not int(_env['DOC']):
    _soft.start()

def push(markerstr:str):
    _soft.push(markerstr)


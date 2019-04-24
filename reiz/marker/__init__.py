from reiz.marker.soft import SoftMarker as _SoftMarker
_soft = _SoftMarker()
_soft.start()

def push(markerstr:str):
    _soft.push(markerstr)


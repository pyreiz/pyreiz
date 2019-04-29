from reiz.marker.standalone import Client as _client
from pylsl import local_clock
# %%

translation = str.maketrans({'ä': 'ae', 'ö': 'oe', 'ü': 'ue',' ':'_'})
def sanitize(marker:str):
   return marker.lower().strip().translate(translation)


def push(marker:str='', tstamp:float=None):
    if tstamp is None:
        tstamp = local_clock()
    marker = sanitize(marker)
    c = _client()
    c.push(marker, tstamp)
    
    

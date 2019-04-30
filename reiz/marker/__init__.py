from reiz.marker.standalone import Client as _client
from pylsl import local_clock
from json import dumps as _dumps
# %%

translation = str.maketrans({'ä': 'ae', 'ö': 'oe', 'ü': 'ue',' ':'_'})
def sanitize_string(marker:str):
   return marker.lower().strip().translate(translation)

def push(marker:str='', tstamp:float=None, sanitize=True):
    if tstamp is None:
        tstamp = local_clock()
    if sanitize:
        marker = sanitize_string(marker)        
    c = _client()
    c.push(marker, tstamp)
    
def push_locals(marker:dict={'key':'value'}, tstamp:float=None, sanitize=False):
    push(_dumps(marker), tstamp, sanitize)
    

from reiz.marker.soft import Client as _client
from pylsl import local_clock
from json import dumps as _dumps
# %%

translation = str.maketrans({'ä': 'ae', 'ö': 'oe', 'ü': 'ue',' ':'_'})
def sanitize_string(marker:str):
   return marker.lower().strip().translate(translation)

def test_connection():
    c = _client()    
    try: 
        c.push('None', local_clock())
        return True
    except ConnectionRefusedError as e:
        print(e)
        input('Please start Markerserver')
        return False
        
def push(marker:str='', tstamp:float=None, sanitize=True):
    if tstamp is None:
        tstamp = local_clock()
    if sanitize:
        marker = sanitize_string(marker)        
    c = _client()
    c.push(marker, tstamp)
    
def push_locals(marker:dict={'key':'value'}, tstamp:float=None, sanitize=False):
    push(_dumps(marker), tstamp, sanitize)
    

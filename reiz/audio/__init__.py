"""
API to auditory stimuli
"""
import pyglet.media.player as _p
Speaker = _p.Player
from reiz.audio._primitives import AudioFile, Hertz

def __get_path():
    import os
    LIBPATH = os.path.dirname(os.path.realpath(__file__))
    LIBPATH = LIBPATH.split(os.path.sep + 'audio')[0]    
    MEDIAPATH = os.path.join(LIBPATH, 'media')              
    return os.path.join(MEDIAPATH, 'wav')
  
PATH = __get_path()

# %%
def __make_library(path=None):
    if path is None:
        path = PATH
    library = dict()
    from types import SimpleNamespace
    import os
    for f in os.listdir(path):
        key = os.path.splitext(f)[0]
        val = AudioFile(os.path.join(path, f))
        library[key] = val
    library = SimpleNamespace(**library)
    return library

library = __make_library()

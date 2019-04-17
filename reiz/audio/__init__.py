"""
API to auditory stimuli
"""
import pyglet.media.player as _p
Speaker = _p.Player
from reiz.audio._primitives import AudioFile, Hertz

def __get_path():
    from reiz import MEDIAPATH
    import os
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

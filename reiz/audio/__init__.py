"""
API to auditory stimuli
"""
from pyglet.media.player import Player as Speaker
from reiz.audio.primitives import AudioFile, Hertz
# %%
def __make_library(path=None):
    if path is None:
        from reiz import AUDIOPATH as path
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
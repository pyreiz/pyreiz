from ._complex import COLORS, Mural, Image, Cross
from ._screen import Canvas

def __get_path():
    from reiz import MEDIAPATH
    import os
    return os.path.join(MEDIAPATH, 'img')
  
PATH = __get_path()


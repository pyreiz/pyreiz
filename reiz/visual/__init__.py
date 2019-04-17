from reiz.visual._complex import COLORS, Mural, Image, Cross
from reiz.visual._screen import Canvas

def __get_path():
    import os
    LIBPATH = os.path.dirname(os.path.realpath(__file__))
    LIBPATH = LIBPATH.split(os.path.sep + 'visual')[0]    
    MEDIAPATH = os.path.join(LIBPATH, 'media')          
    return os.path.join(MEDIAPATH, 'img')
  
PATH = __get_path()
# %%
def __make_library(path=None):
    if path is None:
        path = PATH
        print(path)
    library = dict()
    from types import SimpleNamespace
    import os
    for f in os.listdir(path):
        key, ext = os.path.splitext(f)
        if ext == '.ini':
            import configparser
            ini = configparser.ConfigParser()
            ini.read(os.path.join(path, f))
            opts = ini.options('Murals')
            for o  in opts:                
                val = ini.get('Murals', o)
                library[o] = Mural(val)
        else:
            val = Image(os.path.join(path, f))
            
        library[key] = val
    library = SimpleNamespace(**library)
    return library

library = __make_library()

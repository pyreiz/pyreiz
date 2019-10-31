from reiz.visual._complex import Mural, Image, Cross, Circle, Background, Line, Bar
from reiz.visual._complex import Polygon, Trapezoid, Cylinder

def __get_path():
    import os
    LIBPATH = os.path.dirname(os.path.realpath(__file__))
    LIBPATH = LIBPATH.split(os.path.sep + 'visual')[0]    
    MEDIAPATH = os.path.join(LIBPATH, 'media')          
    return os.path.join(MEDIAPATH, 'img')
  
PATH = __get_path()
# %%
def make_library(path=None):
    'create a library of visual stimuli from path'
    if path is None:
        path = PATH
    library = dict()
    from types import SimpleNamespace
    import os
    for f in os.listdir(path):
        key, ext = os.path.splitext(f)
        if ext == '.ini':
            import configparser, json
            ini = configparser.ConfigParser()
            ini.read(os.path.join(path, f))
            sections = ini.sections();
            if 'Murals' in sections:
                opts = ini.options('Murals')
                for o  in opts:                
                    val = ini.get('Murals', o)
                    library[o] = Mural(**json.loads(val))
                
            if 'Cross' in sections:
                opts = ini.options('Cross')
                for o  in opts:                
                    val = ini.get('Cross', o)
                    library[o] = Cross(**json.loads(val))
   
        else:
            val = Image(os.path.join(path, f))
            key = key.replace("(", "")
            key = key.replace(")", "")
            key = key.replace(" ", "_")
            key = key.replace("-", "_")         
            key = key.strip()
        library[key] = val
    library = SimpleNamespace(**library)
    return library

from os import environ as _env 
if not 'DOC' in _env.keys():
    library = make_library()

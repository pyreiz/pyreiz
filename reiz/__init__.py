# %%
import os 

LIBPATH = os.path.dirname(os.path.realpath(__file__)).split(os.path.sep +
                                                            'experiment')[0]
MEDIAPATH = os.path.join(LIBPATH, 'media')                                                           
del os, LIBPATH
# %% needs to be imported after path construction, as later modules depend on that
import reiz.visual as visual
import reiz.audio as audio
import reiz.marker as marker

#%%
class Cue():
    markerstreamer = marker.SoftMarker()    
    def __init__(self, canvas, audiostim, visualstim, markerstr):
        self.canvas = canvas
        self.audio = audiostim
        self.visual = visualstim
        self.marker = markerstr
        if not self.markerstreamer.is_alive():
            self.markerstreamer.start()
        
    def show(self):
        self.canvas.show(self.visual)
        self.audio.play()
        self.markerstreamer.push(self.marker)
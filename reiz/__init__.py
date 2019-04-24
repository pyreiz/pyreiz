import reiz.visual as visual
import reiz.audio as audio
import reiz.marker as marker
from reiz.time import clock 
#%%
class Cue():
    markerstreamer = marker.SoftMarker()    
    def __init__(self, canvas=None, audiostim=None, 
                 visualstim=None, markerstr=None):
        self.canvas = canvas
        self.audio = audiostim
        self.visual = visualstim
        self.marker = markerstr
        if not self.markerstreamer.is_alive():
            self.markerstreamer.start()
        
    def show(self, canvas=None):
        if canvas is not None:
            self.canvas = canvas
        if self.visual is not None:
            self.canvas.show(self.visual)
        if self.audio is not None:
            self.audio.play()
        if self.marker is not None:
            self.markerstreamer.push(self.marker)
                     
        
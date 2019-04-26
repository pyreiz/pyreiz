import reiz.visual as visual
import reiz.audio as audio
import reiz.marker as marker
from reiz.time import clock 
from reiz.time import Clock  as _Clock
#%%
class Cue():
    def __init__(self, canvas=None, audiostim=None, 
                 visualstim=None, markerstr=None, duration=None):
        self.canvas = canvas
        self.audio = audiostim
        self.visual = visualstim
        self.marker = markerstr
        self.duration = duration
        
    def show(self, canvas=None):
        if canvas is not None:
            self.canvas = canvas
        if self.visual is not None:
            self.canvas.show(self.visual)
        if self.audio is not None:
            self.audio.play()
        if self.marker is not None:
            marker.push(self.marker)

    def show_for(self, duration:float=None, safetime=.2, canvas=None):
        if canvas is not None:
            self.canvas = canvas
        if duration is not None:
            self.duration = duration
            
        clk = _Clock()
        t1 = t0 = clk.time()
        dt = 0
        clk.tick()
        while dt <= self.duration:
            # flipping quantisizes the sleep duration, therefore we 
            # don't flip anymore if that would become relevant
            # we only repeat presentation of the visual stimulus
            # as audio and markers would be senseless and overlays
            if abs(duration-dt) > safetime: 
                self.canvas.show(self.visual)                
                clk.sleep_tick(.1)
            t1 = clk.time()            
            dt = t1-t0             
        return dt
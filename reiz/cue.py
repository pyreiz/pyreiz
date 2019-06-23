#%%
import reiz.marker as marker
from reiz.time import Clock  as _Clock
class Cue():
    def __init__(self, canvas=None, audiostim=None, 
                 visualstim=None, markerstr=None, duration=None):
        self.canvas = canvas
        self.audio = audiostim
        self.visual = visualstim
        self.marker = markerstr
        self.duration = duration
        
    def show(self, canvas=None, duration:float=0, safetime=.2):
        if canvas is not None:
            self.canvas = canvas        
        if self.audio is not None:
            self.audio.play()
        if self.marker is not None:
            marker.push(self.marker)

        if duration is not None:
            self.duration = duration
        
        if self.duration is not None:
            if self.visual is not None and duration==0: #show "forever"
                self.canvas.show(self.visual)
                return 0
            else: #show for duration
                clk = _Clock()
                t1 = t0 = clk.time()
                dt = 0
                clk.tick()
                while dt <= self.duration and self.canvas.available:
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

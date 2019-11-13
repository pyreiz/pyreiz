# -*- coding: utf-8 -*-
"""
LSL based clock

"""

from pylsl import local_clock as _time
# %%
class Clock():
    
    def __init__(self):
        self.time = _time
        self.reset()

    def tick(self):
        ts = self.time()
        delta_t = ts - self.last_ts
        self.cumulative_time += delta_t
        self.last_ts = ts
        return delta_t

    def pause(self):
        ts = self.time()
        delta_t = ts - self.last_ts        
        self.last_ts = ts
        return delta_t
                   
    def reset(self):
        self.cumulative_time = 0
        self.next_ts = self.last_ts = self.time()
        
    def sleep(self, duration):
        t1 = t0 = self.time()
        dt = 0
        while dt <= duration:
            t1 = self.time()            
            dt = t1-t0 
        return dt
    
    def halfsleep(self, duration, canvas, safetime=.2):
        t1 = t0 = self.time()
        dt = 0
        while dt <= duration:
            if abs(duration-dt) > safetime: 
                # flipping quantisizes the sleep duration, therefore we 
                # don't flip anymore if that would become relevant
                canvas.dispatch()
            t1 = self.time()            
            dt = t1-t0             
        return dt
        
    def sleep_tick(self, duration):
        bias = self.tick()
        dt = clock.sleep(duration-bias)
        self.tick()
        return dt

    def __call__(self):
        self.tick()
        return self.cumulative_time
        
    def frames(self, fps=30):
        tick = self.tick()
        return tick*fps
    

clock = Clock()
# %%
if __name__ == '__main__':
    import time
    fps = 30
    cycletime = 1/fps
    clock.reset()
    bias = 0
    clock.tick()
    t0 = clock.time()
    for i in range(0, 90):       
        time.sleep(0.001)
        print(clock.sleep_tick(cycletime))
    print(clock.time()-t0)
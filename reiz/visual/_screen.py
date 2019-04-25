# -*- coding: utf-8 -*-
"""
Pyglet based screen and frame drawing

    
"""
import pyglet            
# %%
def get_screens():
    return pyglet.canvas.Display().get_screens()

# %%
class Canvas():
    def __init__(self, size:(int, int)=(640, 480), origin=(100, 100)):
        maxsize = (get_screens()[0].width, get_screens()[0].height)
        if size == 'full':            
            self.size = maxsize
        else:
            self.size = size    
        
        #check whether origin is outside of window
        outside = [o<0 for o in origin]
        self.origin = [o*(1-c) for o,c in zip(origin, outside)]
        
        self.start_width = size[0]
        self.start_height = size[1]
        self._create_window()
        self.curbuff = 0
               
    def get_fps(self):     
        pyglet.clock.tick()
        for i in range(0, 100, 1):
            self.window.flip()
            pyglet.clock.tick()
        return pyglet.clock.get_fps()
        
    def __enter__(self):
        self.open()
        return self    

    def __exit__(self, type, value, traceback):
        self.close()
    
    def _create_window(self):
        self.window = pyglet.window.Window(visible=False,
                                           vsync=True,
                                           width=self.start_width,
                                           height=self.start_height,
                                           resizable=True,
                                           caption='Experimental Framework')
        self.window.set_location(*self.origin)
        self.window.dispatch_events()
        
            
    def flip(self):
        "flip the backbuffer to front  and clear the old frontbuffer"
        self.window.switch_to()        
        self.window.dispatch_events()
        self.window.dispatch_event('on_draw')
        self.window.flip() # flip front to backbuffer       
        self.window.clear() #clear the current backbuffer: was the old backbuffer
        self.curbuff += 1
        if self.curbuff > 1:
            self.curbuff = 0        
         
    def open(self):  
        if not hasattr(self, 'window'):
            self._create_window()
        self.window.set_visible(True)        
        self.window.switch_to()
        self.window.dispatch_events()
        self.window.dispatch_event('on_draw')
        self.clear()        
    
    def close(self):        
        self.window.close()
        del self.window
    
    def clear(self):    
        "clear both buffers and show a black screen"
        self.flip()
        self.flip()
    
    def show(self, frame):
        "after having rendered and drawn into the backbuffer, show this"
        try:            
            for f in frame:
                if hasattr(f, 'adapt'):
                    f.adapt(self)
                f.draw()
        except TypeError:
            if hasattr(frame, 'adapt'):
                frame.adapt(self)
                frame.draw()
        
        self.flip()
    
    def set_fullscreen(self):   
        #m = pyglet.canvas.Display().get_screens()[monitor]
        #self.window.set_fullscreen(fullscreen=True, screen=m)
        self.window.set_fullscreen(fullscreen=True)
        self.flip()

    def set_windowed(self):
        self.window.set_fullscreen(fullscreen=False)
        self.flip()
        
    def get_width(self):
        return self.window.width
    
    def get_height(self):
        return self.window.height

    def get_diag(self):
        return (self.height * self.width)**0.5
        
    width = property(get_width)
    height = property(get_height)
    diag = property(get_diag)
    
    def run(self):
        pyglet.app.run()
                  

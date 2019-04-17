# -*- coding: utf-8 -*-
"""
test audio stimuli
"""
def test():
    import time
    import reiz.audio
    
    reiz.audio.Hertz().play_blocking()
    reiz.audio.Hertz(frequency=2000, duration_in_ms=2000).play()
    reiz.audio.Hertz(frequency=1000).play()
    time.sleep(2)
    
    ks = reiz.audio.library.__dict__.keys()
    for k in ks:
        if k[0:1] != '_':            
            print(k)
            reiz.audio.library.__dict__[k].play_blocking()            
        
    ks = reiz.audio.library.__dict__.keys()
    for k in ks:
        if k[0:1] != '_':            
            print(k)
            reiz.audio.library.__dict__[k].play()            
      
     
    
if __name__=="__main__":
    '''Example'''
    test()


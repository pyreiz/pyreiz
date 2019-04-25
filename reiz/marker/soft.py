# -*- coding: utf-8 -*-
"""
LSL based software markers
"""

import pylsl
import threading
import queue
import time
# %%
class Outlet():
    instance = None    
    @classmethod
    def get(cls):
        if cls.instance is None:
            import socket, weakref
            source_id = socket.gethostname()
            name = source_id + '-softmarkers'
            info = pylsl.StreamInfo(name, type='Markers', channel_count=1, nominal_srate=0, 
                                    channel_format='string', source_id=source_id)
            outlet = pylsl.StreamOutlet(info)
            cls.instance = weakref.ref(outlet)
        else:
            outlet = cls.instance()
        return outlet

translation = str.maketrans({'ä': 'ae', 'ö': 'oe', 'ü': 'ue',' ':'_'})
def sanitize(marker:str):
   return marker.lower().strip().translate(translation)
    
class SoftMarker(threading.Thread):    
    "LSL based software marker as a singleton, to prevent name-stealing"
    
    
    def __init__(self): 
        threading.Thread.__init__(self)           
        self.queue = queue.Queue(maxsize=0) # indefinite size
        self.is_running = threading.Event()
        
    def push(self, marker:str):
        
        self.queue.put_nowait(sanitize(marker))

    def stop(self):
        self.queue.join()
        self.is_running.clear()
                
    def run(self):
        self._outlet = Outlet.get()
        self.is_running.set()
        while self.is_running.is_set(): 
            try:
                marker = self.queue.get(block=False)
                self._outlet.push_sample([marker])
                self.queue.task_done()
            except queue.Empty:
                time.sleep(0.001)   

# %%
    
def test():
    # %%
    from pylsl import StreamInlet, resolve_stream
    
    # first resolve a marker stream on the lab network
    print("looking for a marker stream...")
    streams = resolve_stream('type', 'Markers')
    
    # create a new inlet to read from the stream
    inlet = StreamInlet(streams[0])
    
    while True:
        # get a new sample (you can also omit the timestamp part if you're not
        # interested in it)
        sample,timestamp = inlet.pull_sample()
        print("got %s at time %s" % (sample[0], timestamp))
        
# %%
if __name__ == '__main__':    
    t = threading.Thread(target=test)
    t.start()
    time.sleep(5)
    sm = SoftMarker()
    sm.start()
    time.sleep(1)
    sm.push('Hallo')    
    time.sleep(1)
    sm.push('Welt')
# -*- coding: utf-8 -*-
"""
LSL based software markers
"""

import pylsl
import threading
import queue
import time
import socket
import json
# %%
class Outlet():
    instance = None    
    @classmethod
    def get(cls, name='reiz_marker'):
        import socket, weakref
        source_id = socket.gethostname()
        if cls.instance is None:                                                
            info = pylsl.StreamInfo(name, type='Markers', channel_count=1, nominal_srate=0, 
                                    channel_format='string', source_id=source_id)
            print(info.as_xml())
            outlet = pylsl.StreamOutlet(info)
            cls.instance = weakref.ref(outlet)
        else:
            outlet = cls.instance()
        return outlet
    
class MarkerStreamer(threading.Thread):    
    "LSL based software marker as a singleton, to prevent name-stealing"

    def __init__(self, name:str=None): 
        threading.Thread.__init__(self)           
        self.queue = queue.Queue(maxsize=0) # indefinite size
        self.is_running = threading.Event()
        self.name = name
        
    def push(self, marker:str='', tstamp:float=None):        
        if marker == '':
            return
        if tstamp is None:
            tstamp = pylsl.local_clock()   
            
        self.queue.put_nowait((marker, tstamp))            
        
    def stop(self):
        self.queue.join()
        self.is_running.clear()
                
    def run(self):        
        self.outlet = Outlet.get(name=self.name)
        self.is_running.set()
        while self.is_running.is_set(): 
            try:
                marker, tstamp = self.queue.get(block=False)
                self.outlet.push_sample([marker], tstamp)
                self.queue.task_done()
                print(f'Pushed {marker} from {tstamp} at {pylsl.local_clock()}')
            except queue.Empty:
                time.sleep(0.001)   

# %%  
def myip():
    """returns the computers default IP address"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

class Client():
    
    def __init__(self,  host:str=None, port:int=7654):
        if host is None:
            host = myip()
        self.host = host
        self.port = port       
        
    def push(self, marker:str='', tstamp:float=None):
        'connects, sends a message, and close the connection'        
        self.connect()
        self.write(marker, tstamp)
        self.close()            
    
    def connect(self):
        'connect wth the remote server'
        self.interface = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.interface.connect((self.host, self.port))
        self.interface.settimeout(3)
  
    def write(self, marker, tstamp):
        'encode message into ascii and send all bytes'        
        msg = json.dumps((marker, tstamp)).encode('ascii')
        print(f'Sending {marker} at {tstamp}')
        self.interface.sendall(msg)

    def close(self):
        'closes the connection'
        self.interface.shutdown(1)
        self.interface.close()

        
class Server(threading.Thread):
    
    def __init__(self, host:str=None, port:int=7654, 
                 name='reiz_marker_sa', timeout=.05):
        threading.Thread.__init__(self)
        self.interface = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.interface.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if host is None:
            host = myip()
        self.host = host
        self.port = port       
        
        self.markerstreamer =  MarkerStreamer(name=name)
        self.markerstreamer.start()
        print(f'Server mediating an LSL Outlet opened at {host}:{port}')
        
    def read_msg(self, client):
        'receive byte for byte to read the header telling the message length'
        #parse the message until it is a valid json 
        msg = bytearray(b' ')
        while True:
            try:
                prt = client.recv(1)                    
                msg += prt                  
                marker, tstamp = json.loads(msg.decode('ascii')) # because the first byte is b' '         
                print(f'Received {marker} for {tstamp} at {pylsl.local_clock()}')
                return marker, tstamp
            except json.decoder.JSONDecodeError:
                pass
            except Exception as e:
                print(e)
                break
            
        return ('', None)

    def stop(self):
        self.is_running = False

    def listen(self):
        'wait for clients to connect and send messages'
        self.interface.bind((self.host, self.port))
        self.interface.listen(1)
        self.is_running = True
        while self.is_running:
            client, address = self.interface.accept()
            client.settimeout(1)
            try:
                print(f'Connected {address}: ', end='')
                marker, tstamp = self.read_msg(client)                
                self.markerstreamer.push(marker, tstamp)
            except socket.timeout:
                print('Client from {address} timed out')
            finally:
                client.shutdown(2)
                client.close()
    
    def start(self):
        self.listen()
# %%
        
# %%
def _test_inlet():
    # %%
    from pylsl import StreamInlet, resolve_stream

    class inletthread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)    
               
        def run(self):
            # first resolve a marker stream on the lab network
            print("looking for a marker stream...")
            streams = resolve_stream('type', 'Markers')           
            # create a new inlet to read from the stream
            inlet = StreamInlet(streams[0])
            self.is_running = True
            while self.is_running:
                # get a new sample (you can also omit the timestamp part if you're not
                # interested in it)
                sample,timestamp = inlet.pull_sample()
                print("got %s at time %s" % (sample[0], timestamp))

        def stop(self):
            self.is_running = False
            print('Listener stopped')
     
    return inletthread() 
    
def _test_outlet():
    time.sleep(5)
    sm = MarkerStreamer()
    sm.start()
    time.sleep(1)
    sm.push('Hallo')    
    sm.push('Welt', None)    
    time.sleep(1)
    sm.push('Timestamp set to 1000', 1000)
# %%
if __name__ == '__main__':
    t = _test_inlet()
    t.start()
    _test_outlet()
    t.stop()

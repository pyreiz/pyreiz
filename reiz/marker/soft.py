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
    "LSL based marker outlet as a singleton, to prevent name-stealing"
    instance = dict()    
    @classmethod
    def get(cls, name='reiz_marker'):
        import socket, weakref
        source_id = "reiz-marker-sa-at-" + socket.gethostname()
        if cls.instance.get(name, None) is None:                                                
            info = pylsl.StreamInfo(name, type='Markers', channel_count=1, nominal_srate=0, 
                                    channel_format='string', source_id=source_id)
            print(info.as_xml())
            outlet = pylsl.StreamOutlet(info)
            cls.instance[name] = weakref.ref(outlet)
        else:
            outlet = cls.instance[name]()
        return outlet
    
class MarkerStreamer(threading.Thread):    
    
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


translation = str.maketrans({'ä': 'ae', 'ö': 'oe', 'ü': 'ue',' ':'_'})
def sanitize_string(marker:str):
   return marker.lower().strip().translate(translation)
        
        
def test_connection(port:int=7654):
    c = Client(port=port)    
    try: 
        c.push('None', pylsl.local_clock())
        return True
    except ConnectionRefusedError as e:
        print(e)
        input('Please start Markerserver')
        return False
    
def ping_connection(port:int=7654):
    c = Client(port=port, verbose=False)    
    try: 
        c.push('None', pylsl.local_clock())
        return True
    except Exception:
        return False

def push(marker:str='', tstamp:float=None, 
        sanitize=True, port:int=7654):
    if tstamp is None:
        tstamp = pylsl.local_clock()
    if sanitize:
        marker = sanitize_string(marker)        
    c = Client(port=port)
    c.push(marker, tstamp)
    
def push_locals(marker:object={'key':'value'}, tstamp:float=None, sanitize=False):
    push(json.dumps(marker), tstamp, sanitize)
    
def push_json(marker:object={'key':'value'}, tstamp:float=None):
    push(json.dumps(marker), tstamp, sanitize=False)
        
class Client():
    
    def __init__(self,  port:int=7654, verbose=True):
        self.host = "127.0.0.1"
        self.port = port       
        self.verbose = verbose
        
    def push(self, marker:str='', tstamp:float=None):
        'connects, sends a message, and close the connection'        
        self.connect()
        self.write(marker, tstamp)
        self.close()            
    
    def connect(self):
        'connect wth the remote server'
        self.interface = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.interface.connect((self.host, self.port))
        self.interface.settimeout(1)
  
    def write(self, marker, tstamp):
        'encode message into ascii and send all bytes'        
        msg = json.dumps((marker, tstamp)).encode('ascii')
        if self.verbose:
            print(f'Sending {marker} at {tstamp}')
        self.interface.sendall(msg)

    def close(self):
        'closes the connection'
        self.interface.shutdown(1)
        self.interface.close()

  
# -----------------------------------------------------------------------------
def read_msg(client):
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
    
class Server(threading.Thread):
    
    def __init__(self, port:int=7654, name='reiz_marker_sa', 
                 timeout=.05):
        threading.Thread.__init__(self)
        self.host = "127.0.0.1"
        self.port = port       
        self.name = name
        self.is_running = threading.Event()      
        self.singleton = threading.Event()      
    
    def stop(self):
        self.is_running.clear()

    def run(self):
        'wait for clients to connect and send messages' 
        if ping_connection(self.port):
            self.singleton.clear()
            print("Server already running on that port")
            self.is_running.set()
            return
        else:
            self.singleton.set()
            print("This server is the original instance")
           
    
        markerstreamer =  MarkerStreamer(name=self.name)
        markerstreamer.start()
        interface = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        interface.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        interface.settimeout(1)
        interface.bind((self.host, self.port))
        interface.listen(1)
        print('Server mediating an LSL Outlet opened at {0}:{1}'.format(
               self.host, self.port))
        self.is_running.set()
        while self.is_running.is_set():
            try:
                client, address = interface.accept()
                try:
                    marker, tstamp = read_msg(client)                    
                    if marker == "None": # connected was only tested 
                        print("Received ping from", address)
                    else:
                        markerstreamer.push(marker, tstamp)
                except socket.timeout:
                    print('Client from {address} timed out')
                finally:
                    client.shutdown(2)
                    client.close()
            except socket.timeout:
                    pass
                
        markerstreamer.stop()

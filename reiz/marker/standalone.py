# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 12:37:23 2019

@author: Trainer
"""
import socket
from reiz.marker.soft import MarkerStreamer
import json
import threading
from pylsl import local_clock
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
        print(f'Sending {msg}')
        self.interface.sendall(msg)

    def close(self):
        'closes the connection'
        self.interface.shutdown(1)
        self.interface.close()

        
class Server(threading.Thread):
    
    def __init__(self, host:str=None, port:int=7654, name='reiz_marker_sa'):
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
                print(f'Received {marker} for {tstamp} at {local_clock()}')
                return marker, tstamp
            except json.decoder.JSONDecodeError:
                pass
            except Exception as e:
                raise e
            
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
                print(f'Connected with client at {address}')
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
                
    
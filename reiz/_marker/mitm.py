# -*- coding: utf-8 -*-
"""
Man-in-the-middle
-----------------

Allows to to manage multiple experiments publishing through one LSL-Outlet and
to create the Outlet independently from starting the experiments to improve
detectability and stability for subscribers (e.g. LabRecorder).

Functions and Classes
.....................
"""

import pylsl
import threading
import queue
import time
import socket
import json
from reiz._marker.client import available
import pkg_resources
version = pkg_resources.get_distribution("reiz").version
# %%


class _Outlet():
    "LSL based marker outlet as a singleton, to prevent name-stealing"
    instance = dict()
    @classmethod
    def get(cls, name='reiz-marker'):
        import socket
        import weakref
        source_id = '_at_'.join((name, socket.gethostname()))
        if cls.instance.get(name, None) is None:
            info = pylsl.StreamInfo(name,
                                    type='Markers',
                                    channel_count=1,
                                    nominal_srate=0,
                                    channel_format='string', source_id=source_id)

            info.desc().append_child_value("version", version)
            print(info.as_xml())
            outlet = pylsl.StreamOutlet(info)
            cls.instance[name] = weakref.ref(outlet)
        else:
            outlet = cls.instance[name]()
        return outlet


class _MarkerStreamer(threading.Thread):

    def __init__(self, name: str = None):
        threading.Thread.__init__(self)
        self.queue = queue.Queue(maxsize=0)  # indefinite size
        self.is_running = threading.Event()
        self.name = name

    def push(self, marker: str = '', tstamp: float = None):
        if marker == '':
            return
        if tstamp is None:
            tstamp = pylsl.local_clock()

        self.queue.put_nowait((marker, tstamp))

    def stop(self):
        self.queue.join()
        self.is_running.clear()

    def run(self):
        self.outlet = _Outlet.get(name=self.name)
        self.is_running.set()
        while self.is_running.is_set():
            try:
                marker, tstamp = self.queue.get(block=False)
                self.outlet.push_sample([marker], tstamp)
                self.queue.task_done()
                print(
                    f'Pushed {marker} from {tstamp} at {pylsl.local_clock()}')
            except queue.Empty:
                time.sleep(0.001)
        print(f"Shutting down MarkerStreamer: {self.name}")
# %%


def myip() -> str:
    """returns a string with the computers default IP address
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


# -----------------------------------------------------------------------------
def _read_msg(client):
    'receive byte for byte to read the header telling the message length'
    # parse the message until it is a valid json
    msg = bytearray(b' ')
    while True:
        try:
            prt = client.recv(1)
            msg += prt
            # because the first byte is b' '
            marker, tstamp = json.loads(msg.decode('ascii'))
            print(f'Received {marker} for {tstamp} at {pylsl.local_clock()}')
            return marker, tstamp
        except json.decoder.JSONDecodeError:
            pass
        except Exception as e:
            print(e)
            break

    return ('', None)


class Server(threading.Thread):
    """Main class to manage the LSL-MarkerStream as man-in-the-middle

    when started, it automatically checks whether there is already a MarkerServer
    running at that port. If this is the case, it returns and lets the old one
    keep control. This ensures that subscribers to the old MarkerServer
    don't experience any hiccups.
    """

    def __init__(self, port: int = 7654, name='reiz-marker',
                 timeout=.05, verbose=True):
        threading.Thread.__init__(self)
        self.host = "127.0.0.1"
        self.port = port
        self.name = name
        self.is_running = threading.Event()
        self.singleton = threading.Event()
        self.verbose = verbose

    def stop(self):
        'stop the server'
        self.is_running.clear()

    def run(self):
        """wait for clients to connect and send messages.

        This is a Thread, so start with :meth:`server.start` """

        # we check whether there is already an instance running, and if so
        # let it keep control by returning
        if available(self.port):
            self.singleton.clear()
            if self.verbose:
                print("Server already running on that port")
            self.is_running.set()
            return
        else:
            self.singleton.set()
            if self.verbose:
                print("This server is the original instance")

        # create the MarkerStreamer, i.e. the LSL-Server that distributes the strings received from the Listener
        markerstreamer = _MarkerStreamer(name=self.name)
        markerstreamer.start()
        # create the ListenerServer, i.e. the TCP/IP Server that waits for messages for forwarding them to the MarkerStreamer
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.settimeout(1)
        listener.bind((self.host, self.port))
        listener.listen(1)
        if self.verbose:
            print('Server mediating an LSL Outlet opened at {0}:{1}'.format(
                self.host, self.port))
        self.is_running.set()
        while self.is_running.is_set():
            try:
                client, address = listener.accept()
                try:
                    marker, tstamp = _read_msg(client)
                    if marker.lower() == "ping":  # connection was only pinged
                        print("Received ping from", address)
                    elif marker.lower() == "poison-pill":
                        print("Swallowing poison pill")
                        self.is_running.clear()
                        break
                    else:
                        markerstreamer.push(marker, tstamp)
                except socket.timeout:
                    print('Client from {address} timed out')
                finally:
                    client.shutdown(2)
                    client.close()
            except socket.timeout:
                pass

        print(f"Shutting down MarkerServer: {self.name}")
        markerstreamer.stop()

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
        import socket
        import weakref
        source_id = '_at_'.join((name, socket.gethostname()))
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
        self.outlet = Outlet.get(name=self.name)
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

# %%


def myip():
    """returns the computers default IP address"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


translation = str.maketrans({'ä': 'ae', 'ö': 'oe', 'ü': 'ue', ' ': '_'})


def sanitize_string(marker: str):
    return marker.lower().strip().translate(translation)


def test_connection(port: int = 7654):
    print("test-connection is deprecated. use available instead")
    return available(port=port)


def available(port: int = 7654, host: str = "127.0.0.1", verbose=True):
    """test whether a markerserver is already available at port

    args
    ----

    host: str 
        the ip of the markerserver (defaults to localhost)

    port: int
        the port number of the markerserver (defaults to 7654)

    returns:

    status:bool
        True if available, False if not
    """
    c = Client(host=host, port=port)
    try:
        c.push('None', pylsl.local_clock())
        return True
    except ConnectionRefusedError as e:
        if verbose:
            print(e)
            print(f'Markerserver at {host}:{port} is not available')
        return False


def ping_connection(port: int = 7654):
    print("ping-connection is deprecated. use available instead")
    c = Client(port=port, verbose=False)
    try:
        c.push('None', pylsl.local_clock())
        return True
    except Exception:
        return False


def push(marker: str = '', tstamp: float = None,
         sanitize=True, port: int = 7654):
    if tstamp is None:
        tstamp = pylsl.local_clock()
    if sanitize:
        marker = sanitize_string(marker)
    c = Client(port=port)
    c.push(marker, tstamp)


def push_locals(marker: object = {'key': 'value'}, tstamp: float = None, sanitize=False):
    push(json.dumps(marker), tstamp, sanitize)


def push_json(marker: object = {'key': 'value'}, tstamp: float = None):
    push(json.dumps(marker), tstamp, sanitize=False)


class Client():

    def __init__(self, host="127.0.0.1", port: int = 7654, verbose=True):
        self.host = host
        self.port = port
        self.verbose = verbose

    def push(self, marker: str = '', tstamp: float = None):
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

    when started, it automatically checks whether there is already a MarkerServer running at that port. If this is the case, it returns and lets the old one keep control. This ensures that possible subscribes to the old 
    MarkerServer don't experience any hiccups.
    """

    def __init__(self, port: int = 7654, name='reiz_marker_sa',
                 timeout=.05, verbose=True):
        threading.Thread.__init__(self)
        self.host = "127.0.0.1"
        self.port = port
        self.name = name
        self.is_running = threading.Event()
        self.singleton = threading.Event()
        self.verbose = verbose

    def stop(self):
        self.is_running.clear()

    def run(self):
        'wait for clients to connect and send messages'

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
        markerstreamer = MarkerStreamer(name=self.name)
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
                    marker, tstamp = read_msg(client)
                    if marker == "None":  # connected was only tested
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


if __name__ == "__main__":
    start()

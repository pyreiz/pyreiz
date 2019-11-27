"""Client interface to the MarkerServer to send markers"""
import pylsl
import socket
import json
from logging import getLogger
log = getLogger()


def sanitize_string(marker: str) -> str:
    """sanitize a string

    removes whitespace, transforms to lower case and replaces umlaute and
    spaces with safer symbols

    args
    ----
    marker:str
        the un-sanitized string

    returns
    -------
    sanitized:str
        the sanitized string
    """
    translation = str.maketrans({'ä': 'ae', 'ö': 'oe', 'ü': 'ue', ' ': '_'})
    marker = marker.lower().strip().translate(translation)

    if marker.lower() == "ping":
        marker = json.dumps({"msg": marker})
        log.critical(
            f"'ping' is a reserved key-word for pinging the marker-server. If you want to ping, use available. Forwarded {marker} instead")
    if marker.lower() == "poison-pill":
        marker = {"msg": marker}
        marker = json.dumps(marker)
        log.critical(
            f"'poison-pill' is a reserved key-word for shutting down the marker-server. If you want to shut-down, use kill. Forwarded {marker} instead")
    return marker


def push(marker: str = '', tstamp: float = None,
         sanitize=True, port: int = 7654):
    """push a marker to the MarkerServer for redistribution as LSL

    args
    ----

    marker: str
        an ascii-encodable string describing an event. We recommend
        to use valid json-strings :func:`~.push_json`
    tstamp: float
        the timestamp of the event. We recommend to use timestamps received
        from pylsl.local_clock
    sanitize: bool
        whether the string is to be sanitized, see :func:`~.sanitize_string`
    port: int
        the port of the MarkerServer

    """
    if tstamp is None:
        tstamp = pylsl.local_clock()
    if sanitize:
        marker = sanitize_string(marker)

    c = _Client(port=port)
    c.push(marker, tstamp)


def push_json(marker: dict = {'key': 'value'}, tstamp: float = None):
    """encode a dictionary as json and push it to the MarkerServer

    args
    ----
    marker:
        a json-encodable dictionary describing an event or current settings
    tstamp:
        the timestamp of the event. We recommend to use timestamps received
        from pylsl.local_clock

    .. caution:
        the resulting msg will not be sanitized :func:`~.sanitize_string`
    """
    push(json.dumps(marker), tstamp, sanitize=False)


def available(port: int = 7654, host: str = "127.0.0.1", verbose=True) -> bool:
    """test whether a markerserver is already available at port

    args
    ----

    host: str
        the ip of the markerserver (defaults to localhost)

    port: int
        the port number of the markerserver (defaults to 7654)

    returns
    -------

    status: bool
        True if available, False if not
    """
    c = _Client(host=host, port=port)
    try:
        c.push('ping', pylsl.local_clock())
        return True
    except ConnectionRefusedError as e:
        if verbose:
            print(e)
            print(f'Markerserver at {host}:{port} is not available')
        return False


def kill(host: str = "127.0.0.1",
         port: int = 7654):
    c = _Client(port=port, host=host)
    c.push("poison-pill",  pylsl.local_clock())


class _Client():
    "Basic Client communicating with the MarkerServer"

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

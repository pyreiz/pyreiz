"""
Safeguard your scripts against absence of a MarkerServer
........................................................


"""
from reiz._marker.mitm import Server
from reiz._marker.client import _Client
from logging import getLogger
logger = getLogger("throw-away-marker-server")

server = None


def available(port: int = 7654, verbose=True) -> bool:
    """test whether a markerserver is already available at port

    Example
    -------

    Protect your script by failing when no marker-server is running.
    .. codeblock:: Python

        if not available():
            print("Start independent markerserver with `reiz-marker`")
            quit()

    args
    ----

    port: int
        the port number of the markerserver (defaults to 7654)

    returns
    -------

    status: bool
        True if available, False if not

    """
    host: str = "127.0.0.1"
    c = _Client(host=host, port=port)
    try:
        c.push('None', pylsl.local_clock())
        return True
    except ConnectionRefusedError as e:
        if verbose:
            print(e)
            print(f'Markerserver at {host}:{port} is not available')
        return False


def start():
    """start a throw-away MarkerServer

    Close it after the experiment with :func:`~.stop`    

    .. caution::
        consider that it is best practice to start an independent MarkerServer to
        improve discoverability and stability for any listeners, especially 
        when recording with LabRecorder. Use these functions only to safeguard 
        your experiment and to be able to test it without the need for an 
        unrelated process running.

    """
    global server
    if server is None or not server.is_running.is_set():
        logger.debug("Starting a throwaway marker-server")
        server = Server(name='reiz_marker_throwaway')
        server.start()
        return server
    else:
        logger.debug("A throwaway marker-server is already running")
        return None


def stop():
    """stop the throw-away MarkerServer

    This MarkerServer was started earlier with :func:`~.start`
    """
    global server
    if server is None:
        logger.debug("No throwaway marker-server is currently running")
        return True
    else:
        server.stop()
        return True

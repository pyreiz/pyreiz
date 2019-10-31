"""
Throw-away MarkerServer
.......................


"""
from reiz._marker.mitm import Server
from logging import getLogger
logger = getLogger("throw-away-marker-server")

server = None


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

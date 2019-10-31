from reiz.marker.soft import Server
from logging import getLogger
logger = getLogger("throw-away-marker-server")

server = None


def start():
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
    global server
    if server is None:
        logger.debug("No throwaway marker-server is currently running")
        return True
    else:
        server.stop()
        return True

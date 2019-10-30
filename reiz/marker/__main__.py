# -*- coding: utf-8 -*-
"""
standalone
"""

import sys
import time
from reiz.marker.soft import Server, test_connection
import argparse


def main():
    parser = argparse.ArgumentParser(description="Reiz Marker Server")
    parser.add_argument("--port", dest="port", type=int,
                        help="Marker Server port.", default=7654)
    parser.add_argument("--name", dest="name",
                        help="Marker Server name.", default='reiz_marker_sa')
    parser.add_argument("--test", action="store_true",
                        help="test connection to Markerserver")
    args = parser.parse_args()
    if args.test:
        test_connection()

    server = Server(port=args.port, name=args.name)
    try:
        server.start()
        while not server.is_running.is_set():
            pass
        if not server.singleton.is_set():
            raise ConnectionAbortedError()
        time.sleep(1)
        print("Server initialized")
        while server.is_running.is_set():
            try:
                pass
            except KeyboardInterrupt:
                break

        server.stop()
        print("\nStreaming stopped.\n")
        server.join()
        print("\nStreaming joined.\n")
        sys.exit(0)

    except ConnectionAbortedError as e:  # erver already connected
        print(e)
        sys.exit(0)


def start():
    import multiprocessing
    return multiprocessing.Process(target=main).start()
    while not reiz.marker.test_connection():
        time.sleep(2)


if __name__ == '__main__':
    main()

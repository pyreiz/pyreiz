# -*- coding: utf-8 -*-
"""
standalone
"""

import sys
import time
from reiz.marker.soft import Server, available
import argparse
import multiprocessing


def main():
    parser = argparse.ArgumentParser(description="Reiz Marker Server")
    parser.add_argument("--port", dest="port", type=int,
                        help="Marker Server port.", default=7654)
    parser.add_argument("--host", dest="host", type=str,
                        help="Marker Server host ip.", default="127.0.0.1")
    parser.add_argument("--name", dest="name",
                        help="Marker Server name.", default='reiz_marker_sa')
    parser.add_argument("--ping", action="store_true",
                        help="test connection to Markerserver")
    args = parser.parse_args()
    if args.ping:
        response = available(host=args.host, port=args.port)
        if response:
            print(f"Markerserver is available at {args.host}:{args.port}")
            sys.exit(0)
        else:
            sys.exit(1)

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
    # multiprocessing.freeze_support() is required in windows
    server = Server()
    server.start()

    while not available():
        time.sleep(2)


if __name__ == '__main__':
    main()

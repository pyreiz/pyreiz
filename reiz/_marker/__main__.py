# -*- coding: utf-8 -*-
"""standalone MarkerServer

run from terminal with
.. codeblock:: bash
    usage: reiz-marker [-h] [--port PORT] [--host HOST] [--name NAME] [--ping]

    Reiz Marker Server

    optional arguments:
    -h, --help   show this help message and exit
    --port PORT  Marker Server port.
    --host HOST  Marker Server host ip.
    --name NAME  Marker Server name.
    --ping       test connection to Markerserver

"""

import sys
import time
from reiz._marker.mitm import Server
from reiz._marker.client import available
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


if __name__ == '__main__':
    main()

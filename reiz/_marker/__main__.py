# -*- coding: utf-8 -*-
"""Standalone MarkerServer

LabRecorder can only start recording Outlets that are existing. If you start a MarkerServer immediatly before you run the experiment, there is not much time for the Recorder to detect the stream.

We there recommend to use a reiz-marker-Server as an independent process. You can either start the MarkerServer as an independent process with `reiz-marker` or `python -m reiz.marker` from your terminal. Shut it down gracefull with `reiz-marker --kill`.

Alternatively, :meth:`~.reiz._marker.safeguard.start` starts such a process from within Python, and you can kill it later with :meth:`~.reiz._marker.safeguard.stop`.

This MarkerServer opens an Outlet that can be detected independently from the experiments you are running. When you then run an experiment, it receives messages from this experiment, and redistributes them in LSL-format.

run from terminal with

.. code-block:: bash

    usage: reiz-marker [-h] [--port PORT] [--host HOST] [--name NAME] [--ping] [--kill]

    Reiz Marker Server

    optional arguments:
    -h, --help   show this help message and exit
    --port PORT  Marker Server port.
    --host HOST  Marker Server host ip.
    --name NAME  Marker Server name.
    --ping       test connection to Markerserver
    --kill       send a poison pill to the Markerserver

"""

import sys
import time
from reiz._marker.mitm import Server
from reiz._marker.client import available, kill
import argparse


def main():

    parser = argparse.ArgumentParser(description="Reiz Marker Server")
    parser.add_argument("--port", dest="port", type=int,
                        help="Marker Server port.", default=7654)
    parser.add_argument("--host", dest="host", type=str,
                        help="Marker Server host ip.", default="127.0.0.1")
    parser.add_argument("--name", dest="name",
                        help="Marker Server name.", default='reiz-marker')
    parser.add_argument("--ping", action="store_true",
                        help="test connection to Markerserver")
    parser.add_argument("--kill", action="store_true",
                        help="send a poison pill to the Markerserver")

    args = parser.parse_args()
    if args.kill:
        if available(host=args.host, port=args.port):
            kill(host=args.host, port=args.port)
        return
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

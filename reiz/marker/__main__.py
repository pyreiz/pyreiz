# -*- coding: utf-8 -*-
"""
standalone
"""

# %%
if __name__ == '__main__':
    import sys
    from reiz.marker.standalone import Server
    import argparse
    parser = argparse.ArgumentParser(description = "Reiz Marker Server")
    parser.add_argument("--host", dest = "host", help="Marker Server IP address.", default=None)
    parser.add_argument("--port", dest = "port", help="Marker Server port.", default=7654)
    parser.add_argument("--name", dest = "name", help="Marker Server name.", default='reiz_marker_sa')
    args = parser.parse_args()
    server = Server(port=args.port, host=args.host, name=args.name)
    server.start()    
    while True:
        try:
            print("Streaming data. Enter 'q' to quit.")
            tmp = input(" > ")
            if tmp == "q":
                server.stop()
                print("\nStreaming stopped.\n")
                sys.exit(0)
        except KeyboardInterrupt:            
            sys.exit(0)
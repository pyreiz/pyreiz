# -*- coding: utf-8 -*-
"""
standalone
"""

# %%
def main():
    import sys
    import time
    from reiz.marker.soft import Server
    import argparse
    parser = argparse.ArgumentParser(description = "Reiz Marker Server")
    parser.add_argument("--port", dest = "port", type=int, help="Marker Server port.", default=7654)
    parser.add_argument("--name", dest = "name", help="Marker Server name.", default='reiz_marker_sa')
    args = parser.parse_args()
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
                print("Streaming data. Enter 'q' to quit.")
                tmp = input(" > ")
                if tmp == "q":
                    break
            except KeyboardInterrupt:
                break
            
        server.stop()
        print("\nStreaming stopped.\n")
        server.join()
        print("\nStreaming joined.\n")        
        sys.exit(0)
    
    except ConnectionAbortedError as e: #erver already connected
        print(e)
        sys.exit(0)

    
def subprocess():
    import multiprocessing
    return multiprocessing.Process(target=main).start()
    
    
if __name__ == '__main__':
    main()


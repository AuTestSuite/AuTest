#start simple server with a time delay
from __future__ import print_function
import time
import sys
import argparse
if sys.version_info >= (3,):
    import http.server as SimpleHTTPServer
    import socketserver as SocketServer
else:
    import SimpleHTTPServer
    import SocketServer


def main( name, wait_time, port ):
    start = time.time()
    print(sys.argv[0], "Delay for:", wait_time, "seconds")
    sys.stderr.flush()
    time.sleep(wait_time)
    SocketServer.TCPServer.allow_reuse_address=True
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", port), Handler)
    print("serving at port", port)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("exiting")
        return

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
        
    parser.add_argument("--time",
                    type=float,
                    help="Time in second to wait before starting server.")

    parser.add_argument("--port",
                    type=int,
                    help="port to run server on.")

    parser.add_argument('-V','--version', action='version', version='%(prog)s 1.0')
    
    args = parser.parse_args()

    main(sys.argv[0],args.time, args.port)

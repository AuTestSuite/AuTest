import socket
import argparse
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', nargs='+', type=int)

    args = parser.parse_args()

    # lifted from When.PortReady's logic
    try:
        for port in args.port:
            # timeout of 1 because we are not doing anything that should take time, so 1 should be enough
            s = socket.create_connection(("127.0.0.1", port), timeout=1)
            s.close()
            print("Connection successful to port {0}!".format(port))
    except:
        print("Wasn't able to connect to port {0}.".format(port))
        print(sys.exc_info()[0])
        exit(1)

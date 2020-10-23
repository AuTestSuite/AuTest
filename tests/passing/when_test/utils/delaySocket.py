import time
import argparse
import threading
import socket


def delayed_listen(s, delay):
    print("Sleeping")
    time.sleep(delay)
    print("Awake, listening now")
    s.listen(500)   # it should be s.listen() but the argument only became optional in python3.5


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', nargs='+', type=int)
    parser.add_argument('--sleep', type=int, default=2)

    args = parser.parse_args()

    print("Got args {0}".format(args.port))

    threads = []
    sockets = []

    # python socket example
    for port in args.port:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('127.0.0.1', port))
        sockets.append(s)
        t = threading.Thread(target=delayed_listen, args=(s, args.sleep,))
        t.daemon = True
        threads.append(t)

    for t in threads:
        t.start()

    while True:
        try:
            time.sleep(.1)
        except KeyboardInterrupt:
            for s in sockets:
                s.close()

            for t in threads:
                t.join()

            break

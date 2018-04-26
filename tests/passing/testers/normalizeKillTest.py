from __future__ import absolute_import, division, print_function
import signal
import time


def sigint_handler(signal, frame):
    print("Ignoring SIGINT")


signal.signal(signal.SIGINT, sigint_handler)

while True:
    time.sleep(1)

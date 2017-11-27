from __future__ import print_function
import sys
from time import sleep
import argparse
import os

def main(name, filename, wait_time):
    if not os.path.isfile(filename):
        print("Error: File {0} does not exist".format(filename) )
    print('Waiting {time} second before removing {file}'.format(time=wait_time, file=filename))
    sleep(wait_time)
    os.remove(filename)    
    print('file has been removed')
    print(name, "Done")


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("filename",
                        type=str,
                        help="Name of the file to modify.")

    parser.add_argument("time",
                        type=float,
                        help="Time in second to wait removing file.")

    parser.add_argument('-V', '--version', action='version',
                        version='%(prog)s 1.0.Beta')

    args = parser.parse_args()

    main(sys.argv[0], args.filename, args.time)

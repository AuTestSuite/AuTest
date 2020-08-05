from __future__ import print_function
from time import sleep
import sys
import argparse


def main(name, filename, wait_time):
    print('Waiting {time} second to open {file}'.format(time=wait_time, file=filename))
    sleep(wait_time)
    f = open(filename, 'w')
    print('file is open: {file}'.format(file=filename))
    f.write('caught at the right time')
    print('First file change: {file}'.format(file=filename))
    f.close()
    sleep(wait_time / 2)
    f = open(filename, 'w')
    f.write('too late now!')
    print('Second file change: {file}'.format(file=filename))
    f.close()
    print(name, "Done")


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("filename",
                        type=str,
                        help="Name of the file to modify.")

    parser.add_argument("time",
                        type=float,
                        help="Time in second to wait before modifying file.")

    parser.add_argument('-V', '--version', action='version',
                        version='%(prog)s 1.0.Beta')

    args = parser.parse_args()

    main(sys.argv[0], args.filename, args.time)

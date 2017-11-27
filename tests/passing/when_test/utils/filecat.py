from __future__ import print_function
import sys
import argparse


def main(name, filename):
    f = open(filename, 'r')
    print(f.readline())
    print('file has been read')
    f.close()
    print(name, "Done")


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("filename",
                        type=str,
                        help="Name of the file to modify.")

    parser.add_argument('-V', '--version', action='version',
                        version='%(prog)s 1.0.Beta')

    args = parser.parse_args()

    main(sys.argv[0], args.filename)


import sys
import argparse
import os


def main(name, directory):
    print(os.listdir(directory))
    print('directory has been read')
    print(name, "Done")


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("directory",
                        type=str,
                        help="Name of the directory to list the contents of.")

    parser.add_argument('-V', '--version', action='version',
                        version='%(prog)s 1.0.Beta')

    args = parser.parse_args()

    main(sys.argv[0], args.directory)

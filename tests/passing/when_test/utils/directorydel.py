
import sys
from time import sleep
import argparse
import os
import shutil


def main(name, directory, wait_time):
    if not os.path.isfile(directory):
        print("Error: Directory {0} does not exist".format(directory))
        sys.exit(1)
    print('Waiting {time} second before removing {dir}'.format(time=wait_time, dir=directory))
    sleep(wait_time)
    shutil.rmtree(directory)
    print('directory has been removed')
    print(name, "Done")


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("directory",
                        type=str,
                        help="Name of the directory to modify.")

    parser.add_argument("time",
                        type=float,
                        help="Time in second to wait removing file.")

    parser.add_argument('-V', '--version', action='version',
                        version='%(prog)s 1.0.Beta')

    args = parser.parse_args()

    main(sys.argv[0], args.directory, args.time)


from time import sleep
import sys
import argparse
import os


def main(name, directory, wait_time):
    print('Waiting {time} second to open {dir}'.format(time=wait_time, dir=directory))
    sleep(wait_time)
    os.mkdir(directory)
    print('directory is created: {dir}'.format(dir=directory))

    first_file = os.path.join(directory, "first_file")
    open(first_file, "w").write('caught at the right time')
    print('First file made under {dir}: {file}'.format(dir=directory, file=first_file))

    sleep(wait_time / 2)

    second_file = os.path.join(directory, "second_file")
    open(second_file, "w").write('too late now!')
    print('Second file made under {dir}: {file}'.format(dir=directory, file=second_file))

    print(name, "Done")


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("directory",
                        type=str,
                        help="Name of the directory to modify.")

    parser.add_argument("time",
                        type=float,
                        help="Time in second to wait before modifying file.")

    parser.add_argument('-V', '--version', action='version',
                        version='%(prog)s 1.0.Beta')

    args = parser.parse_args()

    main(sys.argv[0], args.directory, args.time)

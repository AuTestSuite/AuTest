from __future__ import print_function
import time
import sys
import argparse


def main( name,wait_time ):
    
    start = time.time()
    print(sys.argv[0], "Running for:", wait_time, "seconds")
    while (time.time() - start) < wait_time:
        x = 0
        for i in range(1,100000):
            x+=i
    print(sys.argv[0],"Done")


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
        
    parser.add_argument("time",
                        type=float,
                        help="Time in second to wait.")

    parser.add_argument('-V','--version', action='version', version='%(prog)s 1.0.Beta')
    
    args = parser.parse_args()

    main(sys.argv[0],args.time)

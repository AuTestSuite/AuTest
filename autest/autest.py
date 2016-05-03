# this is the Console Application form of the gtest (gold test) package
from __future__ import absolute_import, division, print_function
import sys
import os
import argparse
from autest.core.engine import Engine
import hosts
import hosts.output
from hosts.console import ConsoleHost


def MakePath(arg):
    path=os.path.abspath(arg)
    if not os.path.exists(path):
        msg='"{0}" is not a valid path'.format(path)
        raise argparse.ArgumentTypeError(msg)
    return path

def JobValues(arg):
    try:
        j=int(arg)
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid int value {0}".format(arg))
    if j==0:
        j=1
    if j < 0:
        msg='Must be a postive value'.format(j)
        raise argparse.ArgumentTypeError(msg)
    return j


if __name__ == '__main__':
    
    # create primary commandline parser
    parser=argparse.ArgumentParser()
    
    parser.add_argument("-D","--directory",
                        type=MakePath,
                        default = os.path.abspath('.'),
                        nargs='?',
                        help="The directory with all the tests in them")

    parser.add_argument("--gtest-site",
                        type=MakePath,
                        nargs='?',
                        help="A user provided gtest-site directory to use instead of the default")

    parser.add_argument("--sandbox",
                        type=os.path.abspath,
                        default = os.path.abspath('./_sandbox'),
                        nargs='?',
                        help="The root directory in which the tests will run")
    
    parser.add_argument("-j","--jobs",
                        default=1,
                        type=JobValues,
                        help="The number of test to try to run at the same time")

    parser.add_argument('-V','--version', action='version', version='%(prog)s 1.0.Beta')
    
   
    # this is a commandline tool so make the cli host
    hosts.setDefaultArgs(parser)
    # make default host
    myhost=hosts.ConsoleHost(parser)
    # setup the extended streams to run
    hosts.Setup(myhost)

    #parser should have all option defined by program and or host type defined
    args=parser.parse_args()
    hosts.output.WriteDebug("init","args=",args)

    #print(args)

    # this is a cli program so we only make one engine and run it
    # a GUI might make a new GUI for every run as it might have new options, or maybe not
    myEngine=Engine(
                   jobs=args.jobs,
                   test_dir=args.directory,
                   run_dir=args.sandbox,
                   gtest_site=args.gtest_site)


    ret=myEngine.Start()
    exit(ret)

    








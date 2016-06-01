# this is the Console Application form of the autest (gold test) package
from __future__ import absolute_import, division, print_function
import sys
import os
import argparse
from autest.core.engine import Engine
import autest.common.execfile as execfile
import hosts
import hosts.output
from hosts.console import ConsoleHost
import copy
import autest
import autest.common.is_a as is_a

#--------------
class extendAction(argparse.Action):
    def __init__( self,
                 option_strings,
                 dest,
                 nargs=None,
                 const=None,
                 default=None,
                 type=None,
                 choices=None,
                 required=False,
                 help=None,
                 metavar=None ):

        if nargs == "?" :
            self.default = default
            raise ValueError('nargs cannot be set to "?" for lists')
        elif is_a.String(nargs) and nargs.isdigit() and int(nargs) <= 1:
            raise ValueError('nargs for extend actions must be greater than 1')
        elif is_a.Int(nargs) and nargs <= 1:
            raise ValueError('nargs for extend actions must be greater than 1')
        elif not is_a.String(nargs) and not is_a.Int(nargs):
            raise ValueError('nargs for extend actions must be a string or int type')

        super(extendAction, self).__init__(option_strings=option_strings,
            dest=dest,
            nargs=nargs,
            const=const,
            default=default,
            type=type,
            choices=choices,
            required=required,
            help=help,
            metavar=metavar)

    def __call__( self, parser, namespace, values, option_string=None ):
        items = []
        for i in values:
            if i[-1] == ',':
                i = i[:-1]
            i = i.split(",")
            items.extend(i)
        setattr(namespace, self.dest, items)


class Settings(object):
    def __init__( self, *args, **kwargs ):
        self.__parser = argparse.ArgumentParser()
        self.__arguments = None
        self.__unknowns = None
        self.__env = None
        return super(Settings, self).__init__(*args, **kwargs)

    @property
    def parser( self ):
        return self.__parser

    @property
    def arguments( self ):
        return self.__arguments
    
    @property
    def unknowns( self ):
        return self.__unknowns

    def finial_parse( self ):
        self.__arguments = self.__parser.parse_args()

    def partial_parse( self ):
        self.__arguments,self.__unknowns = self.__parser.parse_known_args()

    def add_argument( self,arguments, action=None, nargs=None, const=None, default=None, type=None, choices=None, required=None, help=None, metavar=None, dest=None,**kw ):
        
        if action is not None:
            kw['action'] = action
        if nargs is not None:
            kw['nargs'] = nargs
        if const is not None:
            kw['const'] = const
        if default is not None:
            kw['default'] = default
        if type is not None:
            kw['type'] = type
        if choices is not None:
            kw['choices'] = choices
        if required is not None:
            kw['required'] = required
        if help is not None:
            kw['help'] = help
        if metavar is not None:
            kw['metavar'] = metavar
        if dest is not None:
            kw['dest'] = dest
        self.__parser.add_argument(*arguments,**kw) 

    def int_argument( self, arguments, choices=None, default=None, required=None, help=None, metavar=None, dest=None ):
        self.add_argument(arguments, type=int, choices=choices, default=default, required=required, help=help, metavar=metavar, dest=dest)
    def string_argument( self, arguments, default=None, required=None, help=None, metavar=None, dest=None ):
        self.add_argument(arguments, type=str, default=default, required=required, help=help, metavar=metavar, dest=dest)
    def path_argument( self,arguments,default=None,required=None,help=None,metavar=None,dest=None,exists=True ):
        self.add_argument(arguments, type=lambda x: self._path(exists,x), default=default, required=required, help=help, metavar=metavar, dest=dest)
    def bool_argument( self,arguments,default=None,required=None,help=None,metavar=None,dest=None ):
        self.add_argument(arguments, type=self._bool, default=default, required=required, help=help, metavar=metavar, dest=dest)
    def feature_argument( self,feature,default,required=None,help=None,metavar=None ):
        if default != True and default != False:
            hosts.output.WriteError("Default value for feature has to be a True or False value",show_stack=False)
        self.add_argument(["--enable-{0}".format(feature)], action='store_true', default=default, required=required, help=help, metavar=metavar, dest=feature)
        self.add_argument(["--disable-{0}".format(feature)], action='store_false', default=default, required=required, help=help, metavar=metavar, dest=feature)
    
    # add option for mapping x -> y values
    def enum_argument( self, arguments, choices, default=None, required=None, help=None, metavar=None, dest=None ):
        self.add_argument(arguments, choices=choices, type=int, default=default, required=required, help=help, metavar=metavar, dest=dest)
    # add option for mapping x -> y values
    def list_argument( self, arguments,  nargs="*", choices=None, default=None, required=None, help=None, metavar=None, dest=None ):
        self.add_argument(arguments, action=extendAction, nargs=nargs ,choices=choices, type=str, default=default, required=required, help=help, metavar=metavar, dest=dest)

    def get_argument( self, name ):
        return self.__arguments.get(name)

    def _bool( self,arg ):
        
        opt_true_values = set(['y', 'yes', 'true', 't', '1', 'on' , 'all'])
        opt_false_values = set(['n', 'no', 'false', 'f', '0', 'off', 'none'])

        tmp = value.lower()
        if tmp in opt_true_values:
            return True
        elif tmp in opt_false_values:
            return False
        else:
            msg = 'Invalid value Boolean value : "{0}"\n Valid options are {0}'.format(value,
                    opt_true_values | opt_false_values)
            raise argparse.ArgumentTypeError(msg)


    def _path( self, exists, arg ):
        path = os.path.abspath(arg)
        if not os.path.exists(path) and exists:
            msg = '"{0}" is not a valid path'.format(path)
            raise argparse.ArgumentTypeError(msg)
        return path

#----------------------

def JobValues( arg ):
    try:
        j = int(arg)
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid int value {0}".format(arg))
    if j == 0:
        j = 1
    if j < 0:
        msg = 'Must be a postive value'.format(j)
        raise argparse.ArgumentTypeError(msg)
    return j


def main():    
    # create primary commandline parser
    setup = Settings()
    
    setup.path_argument(["-D","--directory"],
                        default = os.path.abspath('.'),
                        help="The directory with all the tests in them")

    setup.path_argument(["--autest-site"],
                        help="A user provided autest-site directory to use instead of the default")

    setup.path_argument(["--sandbox"],
                        default = os.path.abspath('./_sandbox'),
                        exists=False,
                        help="The root directory in which the tests will run")
    
    setup.add_argument(["-j","--jobs"],
                        default=1,
                        type=JobValues,
                        help="The number of test to try to run at the same time")

    setup.list_argument(["--env"],
                        nargs="*",
                        metavar="Key=Value",
                        help="Set a variable to be used in the local test environment. Replaces value inherited from shell.")
    
    setup.list_argument(["-f", "--filters"], 
                        dest='filters',
                        default=['*'],
                        help="Filter the tests run by their names")

    setup.add_argument(['-V','--version'], action='version', version='%(prog)s {0}'.format(autest.__version__))


    # this is a commandline tool so make the cli host
    hosts.setDefaultArgs(setup.parser)
    # make default host
    myhost = hosts.ConsoleHost(setup.parser)
    # setup the extended streams to run
    hosts.Setup(myhost)

    #parser should have all option defined by program and or host type defined
    setup.partial_parse()
    hosts.output.WriteDebugf("init","Before extension load: args = {0}\n unknown = {1}",setup.arguments,setup.unknowns)
    ##-------------------------------------------
    #setup shell environment
    env = os.environ.copy()
    if setup.arguments.env:
        for i in setup.arguments.env:
            try:
                k,v = i.split("=",1)
                env[k] = v
            except ValueError:
                hosts.output.WriteWarning("--env value '{0}' ignored. Needs to in the form of Key=Value".format(i))
    ###-------------------------------------------
    ## look in autest-site directory to see if we have a file to define user options
    if setup.arguments.autest_site is None:
        # this is the default
        path = os.path.join(setup.arguments.directory,'autest-site')
    else:
        #This is a custom location
        path = os.path.abspath(setup.arguments.autest_site)

    ## see if we have a file to load to get new options
    options_file = os.path.join(path,"init.cli.ext")
    if os.path.exists(options_file):
        locals = {'Settings': setup}
        execfile.execFile(options_file,locals,locals)
    ## parse the options and error if we have unknown options
    setup.finial_parse()
    hosts.output.WriteDebugf("init","After extension load: args = {0}",setup.arguments)
    
    ## see if we have any custom setup we want to do globally.
    options_file = os.path.join(path,"setup.cli.ext")
    if os.path.exists(options_file):
        locals = {
            'os':os,
            'ENV': env,
            'Arguments': setup.arguments
            }
        execfile.execFile(options_file,locals,locals)

    # this is a cli program so we only make one engine and run it
    # a GUI might make a new GUI for every run as it might have new options, or maybe not
    myEngine = Engine(jobs=setup.arguments.jobs,
                   test_dir=setup.arguments.directory,
                   run_dir=setup.arguments.sandbox,
                   autest_site=setup.arguments.autest_site,
                   filters=setup.arguments.filters,
                   env=env)

    ret = myEngine.Start()
    exit(ret)

    
if __name__ == '__main__':
    main()







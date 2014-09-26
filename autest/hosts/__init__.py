from .console import ConsoleHost

def setDefaultArgs(argparse):
    defaults = parser.add_argument_group('Console options', 'Arguments unique to console')
    defaults.add_argument("--show-color",
                    action='store_true',
                    help="Show colored output")

    defaults.add_argument("--disable-color",
                    dest='show_color',
                    action='store_false',
                    help="Disable and colored output")
        
    defaults.add_argument("--verbose","-v",
                    action='append',
                    nargs='*',
                    metavar="catagory",
                    help="Display all verbose messages or only messages of provided catagories")

    defaults.add_argument("--debug",
                    action='append',
                    nargs='*',
                    metavar="catagory",
                    help="Display all debug messages or only messages of provided catagories")

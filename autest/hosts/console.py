import sys
import os
import linecache
import colorama

from . import interfaces


class ConsoleHost(interfaces.UIHost):
    """description of class"""
    def __init__(self,parser):
        args=parser.parse_args()
        
        self.__verbose=[] if args.verbose is None else args.verbose
        self.__debug=[] if args.debug is None else args.debug

        if os.name=='nt': 
            colorama.init(wrap=False)
            self.__stdout__= colorama.AnsiToWin32(sys.__stdout__).stream
            self.__stderr__= colorama.AnsiToWin32(sys.__stderr__).stream
        else:
            colorama.init()
            self.__stdout__= sys.__stdout__
            self.__stderr__= sys.__stderr__

#class C io streams
    
    def writeStdOut(self,msg):
        self.__stdout__.write(msg)
            
    def writeStdErr(self,msg):
        self.__stderr__.write(msg)

# our virtual streams
    
    def writeMessage(self,msg):
        self.__stdout__.write(colorama.Style.BRIGHT+msg+colorama.Fore.RESET)

    
    def get_contents(self, filename, lineno):
        content=''
        if lineno > 3:
            content += "  {0}".format(linecache.getline(filename, lineno-3))
        if lineno > 2:
            content += "  {0}".format(linecache.getline(filename, lineno-2))
        if lineno > 1:
            content += "  {0}".format(linecache.getline(filename, lineno-1))
        content += "-> {0}".format(linecache.getline(filename, lineno))
        content += "  {0}".format(linecache.getline(filename, lineno+1))
        return content

    def writeWarning(self,msg,stack=None,show_stack=True):

        self.__stdout__.write(colorama.Fore.LIGHTYELLOW_EX+msg+colorama.Fore.RESET)

    
    def writeError(self,msg,stack=None,show_stack=True):

        self.__stderr__.write(colorama.Fore.LIGHTRED_EX+msg+colorama.Fore.RESET)

    
    def writeDebug(self,catagory,msg):
        '''
        prints a debug message
        catagorty - is the type of verbose message
        msg - is the message to print
        The host may or may not be given all trace messages
        by the engine. The catagory is not added to the message.
        The host can use this value help orginize messages, it is suggested
        that a given message is clearly formatted with the catagory type.
        '''
        self.__stdout__.write(colorama.Fore.GREEN+msg+colorama.Fore.RESET)

    
    def writeVerbose(self,catagory,msg):
        '''
        prints a verbose message
        catagorty - is the type of verbose message
        msg - is the message to print
        The host may or may not be given all verbose messages
        by the engine. The catagory is not added to the message.
        The host can use this value help orginize messages, it is suggested
        that a given message is clearly formatted with the catagory type. 
        '''
        self.__stdout__.write(colorama.Fore.CYAN+msg+colorama.Fore.RESET)

    
    def writeProgress(self,task,msg=None,progress=None,completed=False):
        '''
        task - string telling the current activity we are doing
        status - string telling the current state of the task
        progress - is a value between 0 and 1, -1 means unknown
        completed - tell us to stop displaying the progress

        Will(/might) extend latter with:
        id - an ID that distinguishes each progress bar from the others.
        parentid - tell the parent task to this progress. ( allow formatting improvments to show relationships)
        time_left - a value to tell us an ETA in some time value

        '''
        pass

    @property
    def debugCatagories(self):
        ''' 
        returns list of string defining the catagories of debug messages we want to have 
        processed by the engine
        '''
        return self.__debug

    @property
    def verboseCatagories(self):
        ''' 
        returns list of string defining the catagories of verbose messages we want to have 
        processed by the engine
        '''
        return self.__verbose
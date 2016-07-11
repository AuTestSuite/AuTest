from __future__ import absolute_import, division, print_function
import hosts.output as host
import autest.core.testrunitem as testrunitem
from autest.core.testerset import TesterSet
import autest.testers as testers
import autest.core.order as order
import autest.common.event as event
import autest.core.eventinfo as eventinfo
import autest.core.streamwriter as streamwriter
import autest.common.process
import autest.common.is_a as is_a
from autest.exceptions.killonfailure import KillOnFailureError
from .file import File
import os
import string
import subprocess
import time
import shlex

# deal with subprocess throwing different exceptions on different systems
try: 
    WindowsError 
except NameError: 
    WindowsError = None 


class Process(testrunitem.TestRunItem,order.Order):
    def __init__( self, testrun, name, cmdstr=None,*lst,**kw ):
        super(Process, self).__init__(testrun,*lst,**kw)
        self.__name = name
        self.__cmdstr = cmdstr
        self.__proc = None
        self.__ready = None

        self.__output = None
        self.__stdout = None
        self.__stderr = None

        self.__start_time = None
        self.__last_event_time = None
        # used to help detect if we are taking to long to get ready
        # ie we don't want the isReady test, be it bound to the process
        # or bound as a function of Process A waiting on Process B
        # to take to long else we could deadlock, if the test is never ready
        self.__startup_time = None 
        self.__startup_timeout = None

        # the process environment overrides
        self.__env={}

        self.StartingRun = event.Event()
        self.RunStarted = event.Event()
        self.Running = event.Event()
        self.RunFinished = event.Event()

        self.__streams = object()

        #setup testables
        # ReturnCode
        self._Register(
            "Process.{0}.ReturnCode".format(self.__name),
            TesterSet(
                    testers.Equal,
                    "ReturnCode",
                    self.RunFinished,
                    converter=int,
                    description_group="{0} {1}".format("process",self.Name)
                ),"ReturnCode"
            )
        # TimeOut
        self._Register(
            "Process.{0}.TimeOut".format(self.__name),
            TesterSet(
                    testers.LessThan,
                    "TotalRunTime",
                    self.Running,
                    converter=int,
                    kill_on_failure=True,
                    description_group="{0} {1}".format("process",self.Name)
                ),"TimeOut"
            )
        # Time
        self._Register(
            "Process.{0}.TimeOut".format(self.__name),
            TesterSet(
                    testers.LessThan,
                    "TotalTime",
                    self.RunFinished,
                    converter=int,
                    kill_on_failure=True,
                    description_group="{0} {1}".format("process",self.Name)
                ),"Time"
            )
        # Startup... (remove this one, or make it so we can un bind it during runtime)
    
        
    @property
    def Name( self ):
        return self.__name

    @property
    def Command( self ):
        return self.__cmdstr

    @Command.setter
    def Command( self,value ):
        value = value.replace('/',os.sep)
        self.__cmdstr = value

    @property
    def Env(self):
        return self.__env

    @Env.setter
    def Env(self,val):
        if not is_a.Dict(val):
            raise TypeError("value needs to be a dict type")
        self.__env=val

    # need to remeber if this case is needed
    # ///////////////////////
    @property
    def RawCommand( self ):
        return self.__cmdstr

    @RawCommand.setter
    def RawCommand( self,value ):
        self.__cmdstr = value
    # ////////////////////////

    @property
    def Ready( self ):
        return self.__ready

    @Ready.setter
    def Ready( self,test ):
        if is_a.Number(test):
            host.WriteDebugf(["process"], "Setting ready logic to wait for {0} second for process {1}",test,self.__name)
            self.__ready = lambda : self._hasRunFor(test)
        elif hasattr(test,"when_wrapper"):
            self.__ready = test()
        else:
            self.__ready = test

    def _isReady( self,*lst,**kw ):
        if self.__ready is None:
            return True
        try:
            return self.__ready(*lst,**kw)
        except TypeError:
            return self.__ready()
    
    @property
    def StartupTimeout( self ):
       return self.__startup_timeout

    @StartupTimeout.setter
    def StartupTimeout( self, val ):
        self.__startup_timeout=float(val)

    # internal functions to testing is ready logic
    def _stopReadyTimer( self ):
        self.__startup_time = None

    def _startReadyTimer( self ):
        self.__startup_time = time.time()
    
    def _readyTime( self,curr_time ):
        if self.__startup_time is None:
            return 0.0
        else:
            return curr_time - self.__startup_time
 
    def _hasRunFor( self,t ):
        #Test to see if we have run so long
        host.WriteDebugf(["process"], "Checking if time passed has been {0} seconds", t)
        return (time.time() - self.__start_time) >= t

    def _listcmd(self,cmdstr):
        # hacky function to help deal with command that need a shell without breaking older test files
        lex=shlex.shlex(cmdstr,posix=True)
        #lex.escape+="<>|"
        lex.wordchars+='-$%><&.=:%^'
        lex.commenters=''
        return list(lex)        

    def _isShellCommand(self,cmdstr):
        
        # some command characters that suggest we wanted to run in a shell
        core_operators  = ';&><|'
        shell_args = [';','&&','&','>','>>','<','|','||','cd','set','export',]
        if os.name == 'nt':
            # extra stuff for windows.. not complete, but common stuff
            shell_args = ['echo','dir','del','rmdir','rd','move','rename','mkdir']
        for arg in self._listcmd(cmdstr):
            if arg.lower() in shell_args:
                return True
            # check the arg does not quoted as a string
            # and that it does not contain a core operator
            # allow us to get cases such as 1>&2 like cases
            if arg[0] not in ['"\'']:
                for o in core_operators:
                    if o in arg:
                        return True
        return False

    def _composeEnv(self):
        ret={}
        # get test environment
        ret.update(self._Test.Env)
        # update with with testrun values
        ret.update(self._TestRun.Env)
        # update with process values
        ret.update(self.__env)
        return ret


    # internal functions to control the process
    def _Start( self ):
        if self._isRunning():
            #in case we are already running
            return 
        #create a StreamWriter which will write out the stream data of the run
        #to sorted files
        self.__output = streamwriter.StreamWriter(os.path.join(self._Test.RunDirectory, "_tmp_{0}_{1}_{2}".format(self._Test.Name,self._TestRun.Name,self.__name)),self.Command)
        
        command_line = self.RawCommand

        # substitute the value of the string via the template engine
        # as this provide a safe cross platform $subst model.
        env=self._composeEnv() # get the correct shell env for the process
        template = string.Template(command_line)
        command_line = template.substitute(env)
        
        # test to see that this might need a shell
        try:
            shell = self._isShellCommand(command_line)
        except ValueError as e:
            raise KillOnFailureError(' Bad command line - {1}: {0}'.format(command_line,e))
        args = self._listcmd(command_line) if shell == False else command_line
        
        #call event that we are starting to run the process
        host.WriteDebugf(["process"],"Calling StartingRun event with {0} callbacks mapped to it",len(self.StartingRun))
        self.StartingRun()  
        host.WriteVerbosef(["process"],"Running command:\n '{0}'\n in directory='{1}'\n Path={2}",command_line,self._Test.RunDirectory,env['PATH'])
        host.WriteDebugf(["process"], "Passing arguments to subprocess as: {0}",args)
        if is_a.List(args):
            host.WriteDebugf(["process"], "subprocess list2cmdline = {0}",subprocess.list2cmdline(args))
        try:
            self.__proc = autest.common.process.Popen(args,
                shell=shell,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=self._Test.RunDirectory,
                env=env)
        except IOError as err:
            self.__output.Close()
            self.__output= None
            raise KillOnFailureError('Bad command line - {1}: {0}'.format(command_line,err))
        except OSError as err:
            self.__output.Close()
            self.__output= None
            raise KillOnFailureError('Bad command line - {1}: {0}'.format(command_line,err))
        
        

        # map pipes for output
        self.__stdout = streamwriter.PipeRedirector(self.__proc.stdout, self.__output.WriteStdOut)
        self.__stderr = streamwriter.PipeRedirector(self.__proc.stderr, self.__output.WriteStdErr)

        #Get times
        self.__start_time = time.time()
        self.__last_event_time = self.__start_time

        #set event that process was started
        host.WriteDebugf(["process"],"Calling RunStarted event with {0} callbacks mapped to it",len(self.RunStarted))
        self.RunStarted()


    def _Poll( self ):
        if self._isRunning():
            curr_time = time.time()
            if curr_time - self.__last_event_time > .5:
                #make event info object
                event_info = eventinfo.RunningInfo(self.__start_time,curr_time,self._readyTime(curr_time))
                #call event
                #host.WriteDebugf(["process"],"Process: {0} - Calling Running event with {1} callbacks mapped to it", self.Name ,len(self.Running))
                try:
                    self.Running(event_info)
                except KillOnFailureError:
                    self._kill()
                    raise
                self.__last_event_time = curr_time
            return True
        #We are not running
        # do we need to clean up
        self.__cleanup()

        return False

    def __cleanup( self ):
        if self.__output:
            self.__stdout.close()
            self.__stderr.close()
            self.__output.Close()
            #make event info object
            event_info = eventinfo.FinishedInfo(self.__proc.returncode,time.time() - self.__start_time,self.__output)
            #call event
            host.WriteDebug(["process"],"Calling RunFinished event with {0} callbacks mapped to it".format(len(self.RunFinished)))
            self.RunFinished(event_info)

            self.__stdout = None
            self.__stderr = None
            self.__output = None
            self.__proc = None

    # pull out to base process logic
    def _start( self,*lst,**kw ):
        if self.__proc and self.__proc.poll() is None:
            # we have something running so nothing to start
            return
        self.__proc = autest.common.process.Popen(self.__cmdstr,*lst,**kw)


    def _isRunning( self ):
        return self.__proc is not None and self.__proc.poll() is None

    def _wait( self,timeout ):
        # wait a little while for the process to finish
        # should make this wait time a variable
        self.__proc.waitTimeOut(timeout)
        # if it is not done yet, kill it.
        #if self._isRunning():
            #self.kill()

    def _kill( self ):
        if self._isRunning():
            self.__proc.killtree()
        self.__cleanup()

    # these are to help with discription
    def _isRunningBefore( self ):
            return self._isRunning()
    def _isRunningAfter( self ):
            return self._isRunning()

    

# some forwarding functions...
# for backward compatiblity
def Command( self,cmdstr ):
    self.Processes.Default.Command = cmdstr
def RawCommand( self,cmdstr ):
    self.Processes.Default.RawCommand = cmdstr
def ReturnCode( self,val ):
    self.Processes.Default.ReturnCode = val
def Time( self,val ):
    self.Processes.Default.Time = val
def TimeOut( self,val ):
    self.Processes.Default.TimeOut = val

# for backward compatiblity
class Streams(testrunitem.TestRunItem):
    def __init__( self,testrun ):
        super(Streams, self).__init__(testrun)

    @property
    def stdout( self ):
        return self._TestRun.Processes.Default.Streams.stdout
    @stdout.setter
    def stdout( self,val ):
        self._TestRun.Processes.Default.Streams.stdout = val
    @property
    def stderr( self ):
        return self._TestRun.Processes.Default.Streams.stderr
    @stderr.setter
    def stderr( self,val ):
        self._TestRun.Processes.Default.Streams.stderr = val
    @property
    def All( self ):
        return self._TestRun.Processes.Default.Streams.All
    @All.setter
    def All( self,val ):
        self._TestRun.Processes.Default.Streams.All = val
    @property
    def Warning( self ):
        return self._TestRun.Processes.Default.Streams.Warning
    @Warning.setter
    def Warning( self,val ):
        self._TestRun.Processes.Default.Streams.Warning = val
    @property
    def Error( self ):
        return self._TestRun.Processes.Default.Streams.Error
    @Error.setter
    def Error( self,val ):
        self._TestRun.Processes.Default.Streams.Error = val
    @property
    def Debug( self ):
        return self._TestRun.Processes.Default.Streams.Debug
    @Debug.setter
    def Debug( self,val ):
        self._TestRun.Processes.Default.Streams.Debug = val
    @property
    def Verbose( self ):
        return self._TestRun.Processes.Default.Streams.Verbose
    @Verbose.setter
    def Verbose( self,val ):
        self._TestRun.Processes.Default.Streams.Verbose = val



import autest.api

autest.api.AddTestRunMember(Streams)
autest.api.ExtendTestRun(Command, setproperty=True)
autest.api.ExtendTestRun(RawCommand, setproperty=True)
autest.api.ExtendTestRun(ReturnCode,setproperty=True)
autest.api.ExtendTestRun(Time,setproperty=True)
autest.api.ExtendTestRun(TimeOut,setproperty=True)

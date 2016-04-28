
import autest.core.testrunitem as testrunitem
import autest.testers as testers
import autest.core.order as order
import autest.events as events
from .file import File

import autest.common.process
import os

class Process(testrunitem.TestRunItem):
    def __init__(self, testrun, name, cmdstr=None):
        super(Process, self).__init__(testrun)
        self.__name = name
        self.__cmdstr=cmdstr
        self.__proc=None
    
        self.StartingRun = events.Event()
        self.RunStarted = events.Event()
        self.Running = events.Event()
        self.RunFinished = events.Event()


    @property
    def Command(self):
        return self.__cmd

    @Command.setter
    def Command(self,value):
        value=value.replace('/',os.sep)
        self.__cmd=value

    # need to remeber if this case is needed
    # ///////////////////////
    @property
    def RawCommand(self):
        return self.__cmd

    @RawCommand.setter
    def RawCommand(self,value):
        self.__cmd=value
    # ////////////////////////

    # testable items
    @property
    def ReturnCode(self):
        return self._GetRegisterEvent("Process.{0}.ReturnCode".format(self.__name))

    @ReturnCode.setter
    def ReturnCode(self, val):
        def getChecker():
            if isinstance(val, testers.Tester):
                val.TestValue = 'ReturnCode'
                return val
            else:
                return testers.Equal(int(val), test_value='ReturnCode')
        self._Register("Process.{0}.ReturnCode".format(self.__name), getChecker, event=self.RunFinished)

    @property
    def Time(self):
        return self._GetRegisterEvent("Process.{0}.Time".format(self.__name))

    @Time.setter
    def Time(self, val):
        def getChecker():
            if isinstance(val, testers.Tester):
                val.TestValue = 'TotalTime'
                return val
            else:
                return testers.Equal(int(val), test_value='TotalTime')
        self._Register("Process.{0}.Time".format(self.__name), getChecker, event=self.RunFinished)

    @property
    def TimeOut(self):
        return self._GetRegisterEvent("Process.{0}.TimeOut".format(self.__name))

    @TimeOut.setter
    def TimeOut(self, val):
        def getChecker():
            if isinstance(val, testers.Tester):
                val.TestValue = 'TotalTime'
                return val
            else:
                return testers.LessThan(int(val), test_value='TotalTime', kill=True)
        self._Register("Process.{0}.ReturnCode".format(self.__name), getChecker, event=self.Running)


    # internal functions to control the process

    def _start(self):
        if self.__proc and self.__proc.poll() is None:
            # we have something running so nothing to start
            return
        self.__proc = self.common.process.popen(self.__cmdstr)

    def _isRunning(self):
        return self.__proc.poll() is None

    def _wait(self):
        # wait a little while for the process to finish
        # should make this wait time a variable
        self.__proc.wait(30)
        # if it is not done yet, kill it.
        if self._isRunning():
            self.kill()

    def _kill(self):
        self.__proc.killtree()

    # streams setup (as this is a lot of copy and paste code otherwise
    def __defineProperties__(properties):
        def createStreamProperty(name, event, testValue):
            def getter(self):
                return self._GetRegisterEvent(event)

            def setter(self, value):
                def getChecker():
                    if isinstance(value, testers.Tester):
                        value.TestValue = testValue
                        return value
                    elif isinstance(value, basestring):
                        return testers.GoldFile(File(self._TestRun, value, runtime=False),
                                                test_value=testValue)
                    elif isinstance(value, (tuple, list)):
                        return testers.GoldFileList([File(self._TestRun, item, runtime=False)
                                                     for item in value], test_value=testValue)

                self._Register(event.format(self.__name), getChecker,self._TestRun.EndEvent)

            properties[name] = property(getter, setter)

        STREAMS = (
                   #std streams
                   ('stdout', 'Streams.{0}.stdout', 'StdOutFile'),
                   ('stderr', 'Streams.{0}.stderr', 'StdErrFile'),
                   #filtered streams
                   ('All', 'Streams.{0}.All', 'AllFile'),
                   #('Message', 'Streams.{0).Message', 'MessageFile'), Not sure how to filter this our from stdout
                   ('Warning', 'Streams.{0}.Warning', 'WarningFile'),
                   ('Error', 'Streams.{0}.Error', 'ErrorFile'),
                   ('Debug', 'Streams.{0}.Debug', 'DebugFile'),
                   ('Verbose', 'Streams.{0}.Verbose', 'VerboseFile'),
                  )

        for name, event, testValue in STREAMS:
            createStreamProperty(name, event, testValue)
    __defineProperties__(locals())
    del __defineProperties__


# some forwarding functions...
# for backward compatiblity

def Command(self,cmdstr):
    self.Processes.Default.Command=cmdstr
def ReturnCode(self,val):
    self.Processes.Default.ReturnCode=val
def Time(self,val):
    self.Processes.Default.Time=val
def TimeOut(self,val):
    self.Processes.Default.TimeOut=val

# for backward compatiblity
class Streams(testrunitem.TestRunItem):
    def __init__(self,testrun):
        super(Streams, self).__init__(testrun)

    @property
    def stdout(self):
        return self._TestRun.Processes.Default.stdout
    @stdout.setter
    def stdout(self,val):
        self._TestRun.Processes.Default.stdout=val
    @property
    def stderr(self):
        return self._TestRun.Processes.Default.stderr
    @stderr.setter
    def stderr(self,val):
        self._TestRun.Processes.Default.stderr=val
    @property
    def All(self):
        return self._TestRun.Processes.Default.All
    @All.setter
    def All(self,val):
        self._TestRun.Processes.Default.All=val
    @property
    def Warning(self):
        return self._TestRun.Processes.Default.Warning
    @Warning.setter
    def Warning(self,val):
        self._TestRun.Processes.Default.Warning=val
    @property
    def Error(self):
        return self._TestRun.Processes.Default.Error
    @Error.setter
    def Error(self,val):
        self._TestRun.Processes.Default.Error=val
    @property
    def Debug(self):
        return self._TestRun.Processes.Default.Debug
    @Debug.setter
    def Debug(self,val):
        self._TestRun.Processes.Default.Debug=val
    @property
    def Verbose(self):
        return self._TestRun.Processes.Default.Verbose    
    @Verbose.setter
    def Verbose(self,val):
        self._TestRun.Processes.Default.Verbose=val
    

import autest.api

autest.api.AddTestRunMember(Streams)
autest.api.ExtendTestRun(Command, setproperty=True)
autest.api.ExtendTestRun(ReturnCode,setproperty=True)
autest.api.ExtendTestRun(Time,setproperty=True)
autest.api.ExtendTestRun(TimeOut,setproperty=True)

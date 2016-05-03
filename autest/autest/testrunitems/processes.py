import autest.core.testrunitem as testrunitem
import hosts.output as host
import autest.testers as testers
from .process import Process

class Processes ( testrunitem.TestRunItem ):

    def __init__( self,testrun ):
            super(Processes, self).__init__(testrun)
            self.__processes = {}
            # this the process we will be viewed as the primary process for the
            # test run
            # if not set we will use try to start the correct based on the
            # order logic
            self.__default = None

    def _GetProcesses(self):
        return self.__processes

    def Process( self, id, cmdstr=None, returncode = None ):
        #todo ... add check to make sure id a varaible safe

        tmp = Process(self._TestRun, id, cmdstr)
        if id in self.__processes:
            host.WriteWarning("Overriding process object {0}".format(id))
        self.__processes[id] = tmp
        self.__dict__[id] = tmp
        return tmp

    def Add(self,process):
        if self.process.Name in self.__processes:
            host.WriteWarning("Overriding process object {0}".format(self.process.Name))
        self.__processes[self.process.Name] = self.process
        self.__dict__[self.process.Name] = self.process

    @property
    def Default( self ):
        if self.__default is None:
            self.__default = Process(self._TestRun,name="Default")
        return self.__default

    
def StillRunningBefore(self,process):
    def getChecker():
        if isinstance(process, testers.Tester):
            process.TestValue = process._isRunningBefore
            return process
        else:
            return testers.Equal(True, test_value=process._isRunningBefore)
    self._Register("Process.{0}.RunningStart".format(process.Name), getChecker, event=self.SetupEvent)

def StillRunningAfter(self,process):
    def getChecker():
        if isinstance(process, testers.Tester):
            process.TestValue = process._isRunningAfter
            return process
        else:
            return testers.Equal(True, test_value=process._isRunningAfter)
    self._Register("Process.{0}.RunningAfter".format(process.Name), getChecker, event=self.EndEvent)

def NotRunningBefore(self,process):
    def getChecker():
        if isinstance(process, testers.Tester):
            process.TestValue = process._isRunningBefore
            return process
        else:
            return testers.NotEqual(True, test_value=process._isRunningBefore)
    self._Register("Process.{0}.NotRunningStart".format(process.Name), getChecker, event=self.SetupEvent)

def NotRunningAfter(self,process):
    def getChecker():
        if isinstance(process, testers.Tester):
            process.TestValue = process._isRunningAfter
            return process
        else:
            return testers.NotEqual(True, test_value=process._isRunningAfter)
    self._Register("Process.{0}.NotRunningAfter".format(process.Name), getChecker, event=self.EndEvent)

import autest.api
autest.api.AddTestRunMember(Processes)

autest.api.ExtendTestRun(StillRunningBefore, setproperty=True)
autest.api.ExtendTestRun(StillRunningAfter, setproperty=True)
autest.api.ExtendTestRun(NotRunningBefore, setproperty=True)
autest.api.ExtendTestRun(NotRunningAfter, setproperty=True)

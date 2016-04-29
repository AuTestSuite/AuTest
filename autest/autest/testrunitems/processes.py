import autest.core.testrunitem as testrunitem
import hosts.output as host
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

    def Process( self, cmdstr, id = None, returncode = None ):
        tmp = Process(self._TestRun, id, cmdstr)
        if self.__processes.has_key(cmdstr):
            host.WriteWarning("Overriding process object {0}".format(cmdstr))
        self.__processes[cmdstr] = tmp
            
        if not id:
            host.WriteError("Must provide unique ID value for Process")
        self.__dict__[id] = tmp
        return tmp

    @property
    def Default( self ):
        if self.__default is None:
            self.__default = Process(self._TestRun,name="Default")
        return self.__default


import autest.api
autest.api.AddTestRunMember(Processes)

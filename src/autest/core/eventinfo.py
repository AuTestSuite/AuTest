from __future__ import absolute_import, division, print_function
from autest.common.event import EventInfo

#core test run
class StartInfo(EventInfo):
    def __init__(self,testrun):
        self.__test_run=testrun
   
    @property
    def TestRun(self):
        return self.__test_run


# process events
class StartingInfo(EventInfo):
    def __init__(self):
        pass

class StartedInfo(EventInfo):
    def __init__(self):
        pass

class RunningInfo(EventInfo):
    def __init__(self,start,current,readytime):
        self.startTime=start
        self.currentTime=current
        self.gettingReadyTime=readytime
        return super(RunningInfo, self).__init__()
        
    @property
    def TotalRunTime(self):
        return self.currentTime-self.startTime
    
class FinishedInfo(EventInfo):
    def __init__(self,returncode,runtime,streamwriter):
        self.__returncode=returncode
        self.__runtime=runtime
        self.__all_file=streamwriter.FullFile
        self.__stdout_file=streamwriter.StdOutFile
        self.__stderr_file=streamwriter.StdErrFile
        #self.__message_file=streamwriter.MessageFile
        self.__warning_file=streamwriter.WarningFile
        self.__error_file=streamwriter.ErrorFile
        self.__verbose_file=streamwriter.VerboseFile
        self.__debug_file=streamwriter.DebugFile

    @property
    def TotalRunTime(self):
        return self.__runtime

    @property
    def ReturnCode(self):
        return self.__returncode

    @property
    def AllFile(self):
        return self.__all_file
    @property
    def StdOutFile(self):
        return self.__stdout_file
    @property
    def StdErrFile(self):
        return self.__stderr_file
    @property
    def MessageFile(self):
        return self.__message_file
    @property
    def WarningFile(self):
        return self.__warning_file
    @property
    def ErrorFile(self):
        return self.__error_file
    @property
    def VerboseFile(self):
        return self.__verbose_file
    @property
    def DebugFile(self):
        return self.__debug_file
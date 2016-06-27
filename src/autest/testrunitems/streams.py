from __future__ import absolute_import, division, print_function
import autest.core.testrunitem as testrunitem
import hosts.output as host
import autest.testers as testers
from .file import File

class Streams(testrunitem.TestRunItem):
    def __init__(self,testrun,parent):
        super(Streams, self).__init__(testrun)
        self._process=parent

    # streams setup (as this is a lot of copy and paste code otherwise)    
    def __defineProperties__( properties ):
        def createStreamProperty( name, event, testValue ):
            def getter( self ):
                return self._GetRegisterEvent(event)

            def setter( self, value ):
                def getChecker():
                    if isinstance(value, testers.Tester):
                        value.TestValue = testValue
                        if value.DescriptionGroup is None:
                            value.DescriptionGroup = "{0} {1}".format("process",self._process.Name)
                        return value
                    elif isinstance(value, str):
                        return testers.GoldFile(File(self._TestRun, value, runtime=False),
                                                test_value=testValue,
                                                description_group="{0} {1}".format("process",self._process.Name))
                    elif isinstance(value, (tuple, list)):
                        return testers.GoldFileList([File(self._TestRun, item, runtime=False)
                                                     for item in value], 
                                                     test_value=testValue,
                                                    description_group="{0} {1}".format("process",self._process.Name))

                self._Register(event.format(self._process.Name), getChecker,self._process.RunFinished)

            properties[name] = property(getter, setter)

        STREAMS = (#std streams
                   ('stdout', 'Streams.{0}.stdout', 'StdOutFile'),
                   ('stderr', 'Streams.{0}.stderr', 'StdErrFile'),
                   #filtered streams
                   ('All', 'Streams.{0}.All', 'AllFile'),
                   #('Message', 'Streams.{0).Message', 'MessageFile'), Not sure
                   #how to filter this our from stdout
                   ('Warning', 'Streams.{0}.Warning', 'WarningFile'),
                   ('Error', 'Streams.{0}.Error', 'ErrorFile'),
                   ('Debug', 'Streams.{0}.Debug', 'DebugFile'),
                   ('Verbose', 'Streams.{0}.Verbose', 'VerboseFile'),)

        for name, event, testValue in STREAMS:
            createStreamProperty(name, event, testValue)
    __defineProperties__(locals())
    del __defineProperties__

import autest.api
from . import process
autest.api.AddTestRunMember(Streams,cls=process.Process)


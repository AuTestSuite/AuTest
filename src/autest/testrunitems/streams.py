from __future__ import absolute_import, division, print_function
import autest.core.testrunitem as testrunitem
from autest.core.testerset import TesterSet
import hosts.output as host
import autest.testers as testers
from .file import File

class Streams(testrunitem.TestRunItem):
    def __init__(self,testrun,parent):
        super(Streams, self).__init__(testrun)
        self._process=parent
        
        # setup testers

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
        
        for name, eventname, testValue in STREAMS:
            #tweak to add property for all testable events
            self._Register(
                eventname.format(self._process.Name),
                TesterSet(
                        testers.GoldFile,
                        testValue,
                        self._process.RunFinished,
                        converter=lambda x: File(self._TestRun, x, runtime=False),
                        description_group="{0} {1}".format("process",self._process.Name)
                    ),
                name
                )

import autest.api
from . import process
autest.api.AddTestRunMember(Streams,cls=process.Process)


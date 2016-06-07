import hosts.output as host
from . import tester
from autest.exceptions.killonfailure import KillOnFailureError

import os

class FileExists(tester.Tester):
    def __init__(self,exits,test_value=None,kill_on_failure=False, description_group=None):
        super(FileExists,self).__init__(test_value=test_value,kill_on_failure=kill_on_failure,description_group=description_group)
        self._exits=exits
        if exits:
            self.Description='Checking that file "{0}" exists'.format(tester.get_name(self.TestValue))
        else:
            self.Description='Checking that file "{0}" does not exists'.format(tester.get_name(self.TestValue))

    def test(self, eventinfo, **kw):
        filename=self._GetContent(eventinfo)
        if os.path.isfile(filename):
            if self._exits:
                self.Result=tester.ResultType.Passed
                self.Reason='File "{0}" exists'.format(self.TestValue)
            else:
                self.Result=tester.ResultType.Failed
                self.Reason='File "{0}" exists and it should not'.format(self.TestValue)
        else:
            if self._exits:
                self.Result=tester.ResultType.Failed
                self.Reason='File "{0}" does not exists and it should'.format(self.TestValue)
            else:
                self.Result=tester.ResultType.Passed
                self.Reason='File "{0}" does not exists'.format(self.TestValue)
        host.WriteVerbose(["testers.FileExists","testers"],"Passed - " if self.Result == tester.ResultType.Passed else "Failed - ",self.Reason)

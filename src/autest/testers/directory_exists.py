import hosts.output as host
from . import tester
from autest.exceptions.killonfailure import KillOnFailureError

import os


class DirectoryExists(tester.Tester):
    def __init__(self,exits,test_value=None,kill_on_failure=False, description_group=None):
        super(DirectoryExists,self).__init__(test_value=test_value,kill_on_failure=kill_on_failure,description_group=description_group)
        self._exits=exits
        if exits:
            self.Description='Checking that Directory "{0}" exists'.format(tester.get_name(self.TestValue))
        else:
            self.Description='Checking that Directory "{0}" does not exists'.format(tester.get_name(self.TestValue))

    def test(self, eventinfo, **kw):
        dirname=self._GetContent(eventinfo)
        if os.path.isdir(dirname):
            if self._exits:
                self.Result=tester.ResultType.Passed
                self.Reason='Directory "{0}" exists'.format(dirname)
            else:
                self.Result=tester.ResultType.Failed
                self.Reason='Directory "{0}" exists and it should not'.format(dirname)
        else:
            if self._exits:
                self.Result=tester.ResultType.Failed
                self.Reason='Directory "{0}" does not exists and it should'.format(dirname)
            else:
                self.Result=tester.ResultType.Passed
                self.Reason='Directory "{0}" does not exists'.format(dirname)
        host.WriteVerbose(["testers.directory","testers"],"Passed - " if self.Result == tester.ResultType.Passed else "Failed - ",self.Reason)

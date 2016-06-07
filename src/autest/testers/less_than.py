import hosts.output as host
from . import tester
from autest.exceptions.killonfailure import KillOnFailureError


class LessThan(tester.Tester):

    def __init__( self, value, test_value=None, kill_on_failure=False, description_group=None, description=None ):
        super(LessThan, self).__init__(test_value=test_value, kill_on_failure=kill_on_failure,description_group=description_group,description=description)
        if self.Description is None:   
            self.Description = "Checking that {0} < {1}".format(tester.get_name(test_value), value)
        self._value = value

    def test( self, eventinfo, **kw ):
        # Get value to test against
        val = self._GetContent(eventinfo)
        self.Description=self.Description.format(tester.get_name(self.TestValue),self._value,ev=eventinfo)
        # do test
        if self.DescriptionGroup:
                tmp = self.DescriptionGroup
                des_grp = tmp.format(ev=eventinfo)
        if val >= self._value:
            self.Result = tester.ResultType.Failed
            reason = "Returned value: {0} >= {1}".format(val, self._value)
            self.Reason = reason
            if self.KillOnFailure:
                raise KillOnFailureError
        else:
            self.Result = tester.ResultType.Passed
            self.Reason = "Returned value: {0} < {1}".format(val, self._value)
        host.WriteVerbose(["testers.LessThan", "testers"], "Passed - " if self.Result == tester.ResultType.Passed else "Failed - ", self.Reason)

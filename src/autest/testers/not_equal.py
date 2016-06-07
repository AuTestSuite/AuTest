import hosts.output as host
from . import tester
from autest.exceptions.killonfailure import KillOnFailureError

class NotEqual(tester.Tester):

    def __init__(self, value, test_value=None, kill_on_failure=False,description_group=None):
        super(NotEqual, self).__init__(
            test_value=test_value, kill_on_failure=kill_on_failure,description_group=description_group)
        self.Description = "Checking that {0} != {1}".format(
            tester.get_name(test_value), value)
        self._value = value

    def test(self, eventinfo, **kw):
        # Get value to test against
        val = self._GetContent(eventinfo)
        # do test
        if val == self._value:
            self.Result = tester.ResultType.Failed
            reason = "Returned value: {0} == {1}".format(val, self._value)
            if self.KillOnFailure:                
                raise KillOnFailureError
            self.Reason = reason
        else:
            self.Result = tester.ResultType.Passed
            self.Reason = "Returned value: {0} != {1}".format(val, self._value)
        host.WriteVerbose(["testers.NotEqual", "testers"], "Passed - " if self.Result ==
                          tester.ResultType.Passed else "Failed - ", self.Reason)

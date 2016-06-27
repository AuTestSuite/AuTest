
import hosts.output as host
import re

from . import tester
from autest.exceptions.killonfailure import KillOnFailureError

class ContainsExpression(tester.Tester):
    def __init__(self, regexp, description, killOnFailure = False, description_group = None, reflags=0):
        super(ContainsExpression, self).__init__(
                                    test_value=None,
                                    kill_on_failure=killOnFailure,
                                    description_group=description_group,
                                    description=description
                                    )
        if isinstance(regexp, str):
            if reflags:
                regexp = re.compile(regexp,reflags)
            else:
                regexp = re.compile(regexp)            
        self._multiline = regexp.flags & re.M
        self.__regexp = regexp

    def test(self, eventinfo, **kw):
        filename=self._GetContent(eventinfo)
        if filename is None:
            filename = self.TestValue.AbsPath
        result = tester.ResultType.Passed
        try:
            passed = False
            # if this is multi-line check
            if self._multiline:
                with open(filename, 'r') as infile:
                    data = infile.read()
                passed = self.__regexp.search(data)
            else:
                # if this is single expression check each line till match
                with open(filename, 'r') as infile:
                    for l in infile:
                        # need to check all line as on line has to hit
                        passed = self.__regexp.search(l)
                        if passed:
                            break
            if not passed:
                result = tester.ResultType.Failed
                self.Reason = 'Contents of {0} did not contains expression: "{1}"'.\
                              format(filename, self.__regexp.pattern)
        except IOError as err:
            result = tester.ResultType.Failed
            self.Reason = 'Cannot read {0}: {1}'.format(filename, err)

        self.Result = result
        if result != tester.ResultType.Passed:
            if self.KillOnFailure:
                raise KillOnFailureError
        else:
            self.Reason = 'Contents of {0} contained expression'.format(filename)
        host.WriteVerbose(["testers.ContainsExpression","ContainsExpression"],"Passed - " if self.Result == tester.ResultType.Passed else "Failed - ",self.Reason)

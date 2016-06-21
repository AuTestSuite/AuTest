import hosts.output as host
from . import tester
from autest.exceptions.killonfailure import KillOnFailureError

class Lambda(tester.Tester):
    def __init__( self,func,kill_on_failure=False):
        super(Lambda,self).__init__(func, kill_on_failure=kill_on_failure)
        self._func = func
        
    def test( self,eventinfo, **kw ):
        # run the test function
        result,message = self._func(eventinfo)
        self.Reason = message
        # process results
        if result:            
            self.Result = tester.ResultType.Failed
            if self.KillOnFailure:
                raise KillOnFailureError        
        else:
            self.Result = tester.ResultType.Passed
        host.WriteVerbose(["testers.GreaterThan","testers"],"Passed - " if self.Result == tester.ResultType.Passed else "Failed - ",self.Reason)

from __future__ import absolute_import, division, print_function

# This class is for all the objects we add to a testrun object
# It contains a interface that allows us to forward call to the main 
# TestRun object
class TestRunItem(object):
    def __init__(self,testrun,*lst,**kw):
        self.__testrun=testrun
        super(TestRunItem, self).__init__()

    @property
    def _TestRun(self):
        return self.__testrun

    @property
    def _Test(self):
        return self.__testrun._Test

    def _Register(self, key, validateCallback, event):
        #forward call to main TestRun object
        # this registers the "test" object so we can get 
        # the results later
        self._TestRun._Register(key,validateCallback,event)

from __future__ import absolute_import, division, print_function
from future.utils import with_metaclass
import autest.glb as glb

class _testrun_item__metaclass__(type):
    def __call__(cls,*lst,**kw):
        #make instance of the class
        inst=type.__call__(cls,*lst,**kw)
        # given which class this is we look up 
        # in a dictionary which items we want to add
        cls_info=glb._runtest_items.get(cls,{})
        # add any items we want to add to the runtest item.
        for k,v in cls_info.items():
            setattr(inst,k,v(inst._TestRun,inst))
        return inst

# This class is for all the objects we add to a testrun object
# It contains a interface that allows us to forward call to the main 
# TestRun object
class TestRunItem((with_metaclass(_testrun_item__metaclass__,object))):
    def __init__(self,testrun,*lst,**kw):
        self.__testrun=testrun
        super(TestRunItem, self).__init__()

    @property
    def _TestRun(self):
        return self.__testrun

    @property
    def _Test(self):
        return self.__testrun._Test

    def _Register(self,event_name,event_callbacks,property_name):
        #forward call to main TestRun object
        # this registers the "test" object so we can get 
        # the results later
        return self._TestRun._Register(event_name,event_callbacks,property_name,self)

    def _GetRegisteredEvent( self, key ):
        return self._TestRun._GetRegisteredEvent(key)


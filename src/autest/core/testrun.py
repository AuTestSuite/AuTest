from __future__ import absolute_import, division, print_function
import autest.glb as glb
import hosts.output as host
import autest.common.event as event
import autest.common as common
import autest.common.is_a as is_a
import autest.testers as testers
from autest.core.testerset import TesterSet
from future.utils import with_metaclass

import pprint
# this is base class to add common logic for when I need to
# delay adding the event mapping.  The reasonf or this woudl be cases
# in which more than one value coudl be mapped in a file, but only on can exist in the event
# in cases like this we can make sure the correct logic exists for mapping the first
# or last value only.  Likewise handling cases in which I would want to make more than one
# event can be handled correctly as well.  The second factor this adds is some debug ablity
# on what is being mapped to the event


#todo ..  move to independent file...
class DelayedEventMapper(object):
    '''
    This class provides the base interface for creating predefined event mappings for a
    defined concept
    '''
    __slots__ = ['__addevent']

    def __init__( self ):
        self.__addevent = {}

    def _Register( self,event_name,event_callbacks,property_name,inst=None):
        if inst is None:
            inst=self
        cls=inst.__class__
        varname="_event_name_{0}_".format(property_name)
        setattr(inst,varname,event_name)
        self.__addevent[event_name] = event_callbacks
        def getter( self ):
            return self._GetRegisteredEvent(getattr(self,varname))

        def setter( self,value ):
            if not isinstance(value, TesterSet):
                obj = self._GetRegisteredEvent(getattr(self,varname))
                if is_a.List(value):
                    for v in value:
                        obj.add(v)
                else:
                    obj.assign(value)
                

        property_name = common.make_list(property_name)
        for p in property_name:
            if not hasattr(cls,p):
                setattr(cls,p,property(getter, setter))

    def _BindEvents( self ):
        '''
        Bind the event to the callbacks
        '''
        for obj in self.__addevent.values():
            if not isinstance(obj, TesterSet):
                event,callback = obj
                event += callback
            else:
                obj._bind()
            
        #for event, callback in self.__addevent.values():
            #event += callback

    def _GetCallBacks( self ):        
        return self.__addevent.values()            

    def _RegisterEvent( self, key, event, callback ):
        '''
        Default set or override "named" event
        '''
        if key in self.__addevent:
            host.WriteDebug(['testrun'],"Replacing existing key: {0} value: {1} with\n new value: {2}".format(key,self.__addevent[key],(event, callback)))
        self.__addevent[key] = (event, callback)

    #def _AddRegisterEvent( self, key, event, callback ):
    #    '''
    #    Default set or override "named" event
    #    '''
    #    self.__addevent[key] += (event, callback)

    def dump_event_data( self ):
        ret = ""
        for k,v in self.__addevent.items():
            if isinstance(v, TesterSet):
                if len(v._testers):
                    ret+=k + ":\n"
                    ret+="  " + pprint.pformat(v._testers,indent=2) + "\n"
            else:
                ret+=k + ":\n"
                ret+="  {0}\n".format(v)
        return ret

    def _GetRegisteredEvent( self, key ):
        ''' 
        return a given event mapping so we can add on to it
        '''
        try:
            return self.__addevent[key]
        except KeyError:
            return None

    def _GetRegisteredEvents( self ):
        return self.__addevent

class _testrun__metaclass__(type):
    def __call__( cls,*lst,**kw ):
        #make instance of the class
        inst = type.__call__(cls,*lst,**kw)
        # given which class this is we look up
        # in a dictionary which items we want to add
        cls_info = glb._runtest_items.get(cls,{})
        # add any items we want to add to the runtest item.
        for k,v in cls_info.items():
            setattr(inst,k,v(inst))
        return inst

class BaseTestRun(with_metaclass(_testrun__metaclass__,DelayedEventMapper)):
    def __init__( self, testobj, name, displaystr ):
        self.__displaystr = displaystr # what we display to the user
        self.__name = name # that name of this test run
        self.__test = testobj # this is the parent test object
        self.__exceptionMessage = '' # this is a error message given an unknown exeception

        # this is the result type of the test run
        self.__result = None 

        # core events
        self.__SetupEvent = event.Event()
        self.__StartEvent = event.Event()
        self.__EndEvent = event.Event()

        self.__env={}
                

        #self.__concepts = [] # test run concepts to add to dynamically mix in
        super(BaseTestRun, self).__init__()

 # attributes of this given test run
    @property
    def Name( self ):
        return self.__name

    @property
    def DisplayString( self ):
        if self._displaystr:
            return self._displaystr
        return self.name

    @DisplayString.setter
    def DisplayString( self ):
        if self.__displaystr:
            return self.__displaystr
        return self.Name

    @property
    def Env(self):
        return self.__env

    @Env.setter
    def Env(self,val):
        if not is_a.Dict(val):
            raise TypeError("value needs to be a dict type")
        self.__env=val

    #event accessors
    @property
    def SetupEvent( self ):
        return self.__SetupEvent
    @property
    def StartEvent( self ):
        return self.__StartEvent
    @property
    def EndEvent( self ):
        return self.__EndEvent

    @property
    def _Result( self ):
        if self.__result is None:
            self.__result = -1
            for i in self._getTesters():
                if self.__result < i.Result:
                    self.__result = i.Result
        #if we are have no result and have nothing to test
        # we say we passed
        if self.__result == -1 and len(self._getTesters()) == 0:
            self.__result = testers.ResultType.Passed
        return self.__result

    @_Result.setter
    def _Result( self,val ):
        self.__result = val

    @property
    def _ExceptionMessage( self ):
        if self._Result == testers.ResultType.Exception and self.__exceptionMessage == "":
            for i in self._getTesters():
                if i.Result == testers.ResultType.Exception:
                    self.__exceptionMessage = i.Reason
        return self.__exceptionMessage

    @_ExceptionMessage.setter
    def _ExceptionMessage( self,val ):
        self.__exceptionMessage = val

    def _getTesters( self ):
        ret = []
        for x in self._GetCallBacks():
            if not isinstance(x, TesterSet):
                ret.append(x[1])
            else:
                ret+=[t for t in x._testers if isinstance(t, testers.tester.Tester)]
        return ret
        
    @property
    def _Test( self ):
        return self.__test


class TestRun(BaseTestRun):
    def __init__( self, testobj, name, displaystr ):
        super(TestRun, self).__init__(testobj, name, displaystr)

        # setup testables
         ## util object
        class LamdaEq(object):
            def __init__(self, func):
                self.__func=func
            def __eq__(self,rhs):
                return self.__func() == rhs
            def __ne__(self,rhs):
                return self.__func() != rhs

        # StillRunningBefore
        self._Register(
            "Test.Process.StillRunningBefore",
            TesterSet(
                    testers.Equal,
                    True,
                    self.SetupEvent,
                    converter=lambda val: LamdaEq(val._isRunningBefore),
                ),"StillRunningBefore"
            )
        # StillRunningAfter
        self._Register(
            "Test.Process.StillRunningAfter",
            TesterSet(
                    testers.Equal,
                    True,
                    self.EndEvent,
                    converter=lambda val: LamdaEq(val._isRunningBefore),
                ),"StillRunningAfter"
            )
        # NotRunningBefore
        self._Register(
            "Test.Process.NotRunningBefore",
            TesterSet(
                    testers.Equal,
                    False,
                    self.SetupEvent,
                    converter=lambda val: LamdaEq(val._isRunningBefore),
                ),"NotRunningBefore"
            )
        # NotRunningAfter
        self._Register(
            "Test.Process.NotRunningAfter",
            TesterSet(
                    testers.Equal,
                    False,
                    self.EndEvent,
                    converter=lambda val: LamdaEq(val._isRunningBefore),
                ),"NotRunningAfter"
            )
        

    


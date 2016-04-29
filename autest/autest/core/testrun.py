
import autest.glb as glb
import hosts.output as host
import autest.common.event as event
import autest.testers as testers

# this is base class to add common logic for when I need to
# delay adding the event mapping. The reasonf or this woudl be cases
# in which more than one value coudl be mapped in a file, but only on can exist in the event
# in cases like this we can make sure the correct logic exists for mapping the first
# or last value only. Likewise handling cases in which I would want to make more than one
# event can be handled correctly as well. The second factor this adds is some debug ablity
# on what is being mapped to the event

#todo .. move to independent file...
class DelayedEventMapper ( object ):
    '''
    This class provides the base interface for creating predefined event mappings for a
    defined concept
    '''
    __slots__ = ['__addevent']

    def __init__( self ):
        self.__addevent = {}

    def _BindEvents( self ):
        '''
        Bind the event to the callbacks
        '''
        for event, callback in self.__addevent.itervalues():
            event += callback

    def _GetCallBacks(self):
        ret=[]
        for v in self.__addevent.viewvalues():
            ret.append(v[1])
        return ret

    def _RegisterEvent( self, key, event, callback ):
        '''
        Default set or override "named" event
        '''
        if self.__addevent.has_key(key):
            host.WriteDebug(['testrun'],"Replacing existing key: {0} value: {1} with\n new value: {2}".format(key,self.__addevent[key],(event, callback)))
        self.__addevent[key] = (event, callback)

    def _AddRegisterEvent( self, key, event, callback ):
        '''
        Default set or override "named" event
        '''
        self.__addevent[key] += (event, callback)

    def _GetRegisteredEvent( self, key ):
        ''' 
        return a given event mapping so we can add on to it
        '''
        try:
            return self.__addevent[key]
        except KeyError:
            return None

    def _GetRegisteredEvents(self):
        return self.__addevent

    def _Register( self, key, validateCallback, event ):
        try:
            # call callback to verify type is correct
            checker = validateCallback()            
            if checker:
                self._RegisterEvent(key, event, checker)
            else:
                host.WriteError('Invalid type')
        except BaseException, err:
            import traceback
            host.WriteError('Exception occurred: {0}'.format(traceback.format_exc()))


class _testrun__metaclass__(type):
        def __call__(cls,*lst,**kw):
            #make instal of the class
            inst=type.__call__(cls,*lst,**kw)
            # given which class this is we look up 
            # in a dictionary which items we want to add
            cls_info=glb._runtest_items.get(cls,{})
            # add any items we want to add to the runtest item.
            for k,v in cls_info.iteritems():
                setattr(inst,k,v(inst))
            return inst

class BaseTestRun (DelayedEventMapper):

    __metaclass__=_testrun__metaclass__

    def __init__( self, testobj, name, displaystr ):
        self.__displaystr = displaystr # what we display to the user
        self.__name = name # that name of this test run
        self.__test = testobj # this is the parent test object
        self.__exceptionMessage = '' # this is a error message given an unknown exeception

        # this is the result type of the test run
        self.__result=None 

        # core events
        self.__SetupEvent = event.Event()
        self.__StartEvent = event.Event()
        self.__EndEvent = event.Event()
                

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
    def _Result(self):
        if self.__result is None:
            for i in self._getTesters():
                if self.__result < i.Result:
                    self.__result = i.Result
        #if we are have no result and have nothing to test
        # we say we passed
        if self.__result is None and len(self._getTesters()) == 0:
            self.__result = testers.ResultType.Passed
        return self.__result

    @_Result.setter
    def _Result(self,val):
        self.__result=val

    @property
    def _ExceptionMessage(self):
        if self._Result == testers.ResultType.Exception and self.__exceptionMessage=="":
            for i in self._getTesters():
                if i.Result == testers.ResultType.Exception:
                    self.__exceptionMessage = i.Reason
        return self.__exceptionMessage

    @_ExceptionMessage.setter
    def _ExceptionMessage(self,val):
        self.__exceptionMessage=val;


    def _getTesters(self):
        return self._GetCallBacks()

    @property
    def _Test(self):
        return self.__test


class TestRun (BaseTestRun ):
    def __init__( self, testobj, name, displaystr ):
        super(TestRun, self).__init__(testobj, name, displaystr)

    


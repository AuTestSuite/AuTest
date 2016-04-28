
import autest.glb as glb
import autest.exceptions.setuperror as setuperror

class _setup__metaclass__(type):
        def __call__(cls,*lst,**kw):
            inst=type.__call__(cls,*lst,**kw)
            for k,v in glb._setup_items.iteritems():
                setattr(inst,k,v(inst))
            return inst

class Setup(object):
    __metaclass__=_setup__metaclass__

    def __init__(self,test):
        self.__setup_items=[]
        self.__test=test
        self.__reason=None
    
    def _add_item(self,task):
        # bind the setup task with the test object so it 
        # can get information about certain locations
        task._bind(self.__test)
        self.__setup_items.append(task)

    def _get_items(self):
        return self.__setup_items

    def _do_setup(self):
        items=self._get_items()
        try:
            for i in items:
                i.setup()
        except setuperror.SetupError, e:
            self.__reason=str(e)
            raise 

    def _do_cleanup(self):
        items=self.__test.Setup._get_items()
        try:
            for t in items:
                t.cleanup() 
        except setuperror.SetupError, e:
            self.__reason=str(e)
            raise e
    @property
    def _Reason(self):
        if not self.__reason:
            return "Setup has no issues"
        return self.__reason
    
    @_Reason.setter
    def _Reason(self, value):
        self.__reason = value

    @property
    def _Failed(self):
        return self.__reason is not None

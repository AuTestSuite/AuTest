from __future__ import absolute_import, division, print_function
from . import setup
from . import conditions
from . import testrun
from .runable import Runable
from .order import Order
from .item import Item
import autest.common.is_a as is_a
import autest.testers.tester as testers
from autest.common.constructor import call_base, smart_init

import os
    
@smart_init
class Test(Runable,Order,Item):
    __slots__ = ["__run_serial",
            "__setup",
            "__test_runs",
            "__test_dir",
            "__test_file",
            "__test_root",
            "__run_dir",
            "__result",
            "__processes",
            "__conditions",]

    @call_base(Runable=(None,),Order=(),Item=(None,"id"))
    def __init__(self,id,test_dir,test_file,run_root,test_root,env,variables):
        self.__run_serial = False

        ##internal data
        # the different test runs
        self.__test_runs = [] 
        # this is the location of the test file
        self.__test_dir = test_dir
        #this is the name of the test file
        self.__test_file = test_file
        #this is the directory we scanned to find this test
        self.__test_root = test_root
        #this is the directory we will run the test in
        self.__run_dir = os.path.normpath(os.path.join(run_root, id))
        #this is the result of the test ( did it pass, fail, etc...)
        self.__result = None
        #controls is we should continue on a failure
        self.__continueonfail = False

        ## this is a bit of a hack as this hard coded in..  try to address later
        # this is the set of extra processes that we might need running
        #for the test to work
        #self.__processes=Processes(self)

        # property objects
        self.__setup = setup.Setup(self)
        self.__conditions = conditions.Conditions()

        # make a copy of the environment so we can modify it without issue
        self.Env = env
        #add some default values
        self.Env['AUTEST_TEST_ROOT_DIR'] = self.__test_root
        self.Env['AUTEST_TEST_DIR'] = self.__test_dir
        self.Env['AUTEST_RUN_DIR'] = self.__run_dir
        # additional variables
        self.Variables = variables

# public properties
    @property
    def Name(self):
        return self._ID

    @Name.setter
    def Name(self,val):
        self._ID = val

    @property
    def Summary(self):
        return self._Description

    @Summary.setter
    def Summary(self,val):
        self._Description = val

    @property
    def RunSerial(self):
        return self.__run_serial

    @RunSerial.setter
    def RunSerial(self,val):
        self.__run_serial = val

    @property
    def Setup(self):
        return self.__setup

    def SkipIf(self,*lst):
        return self.__conditions._AddConditionIf(lst)

    def SkipUnless(self,*lst):
        return self.__conditions._AddConditionUnless(lst)

    @property
    def TestDirectory(self):
        return self.__test_dir

    @property
    def TestFile(self):
        return self.__test_file

    @property
    def TestRoot(self):
        return self.__test_root

    @property
    def RunDirectory(self):
        return self.__run_dir
  
    # public methods
    def AddTestRun(self, name='general', displaystr=None):
        tmp = testrun.TestRun(self, "%s-%s" % (len(self._TestRuns), name), displaystr)
        self._TestRuns.append(tmp)
        return tmp
   
    #internal stuff

    @property
    def _TestRuns(self):
        return self.__test_runs

    @property
    def _Conditions(self):
        return self.__conditions

    @property
    def _ChildRunables(self):
        return self.Setup._Items + list(self.Processes._Items) + self.__test_runs
    
    @property
    def ContinueOnFail(self):
        return self.__continueonfail

    @ContinueOnFail.setter
    def ContinueOnFail(self,val):
        self.__continueonfail = val

#class Processes ( object ):

#    def __init__( self,test):
#            super(Processes, self).__init__()
#            # special testrun object to allow for global processes
#            # probally should split the process object better
#            self._TestRun=testrun.TestRun(test, "_Global", "Global Processes")
#            self.__Test=test
#            self.__processes = {}
#            # this the process we will be viewed as the primary process for the
#            # test run
#            # if not set we will use try to start the correct based on the
#            # order logic
#            self.__default = None

#    def _GetProcesses(self):
#        return self.__processes.values()

#    def Process( self, id, cmdstr=None, returncode = None, startup_timeout=10, ready=None ):
#        from autest.testenity.process import Process
#        #todo ... add check to make sure id a variable safe

#        tmp = Process(self._TestRun, id, cmdstr)

#        if returncode is not None:
#            tmp.ReturnCode=returncode
#        tmp.StartupTimeout=startup_timeout

#        # todo ... add valation to ready for type?
#        if ready is not None:
#            tmp.Ready=ready
        

#        if id in self.__processes:
#            host.WriteWarning("Overriding process object {0}".format(id))
#        self.__processes[id] = tmp
#        self.__dict__[id] = tmp
#        return tmp

#class Test(RunableScoped,Order):
#    """Defines a test.
#    A test contains a list of test runs objects,
#    information about the test, such as name, discription,
#    can the test run in threaded with other tests and a
#    setup/clean up object to help control the environment 
#    the test will run in
#    """
#    #__slots__=[]
    
#    def __init__(self, name, test_dir, test_file, run_root, test_root, env, variables):
#        # traits
#        self.__run_serial=False
#        self.__summary=''
#        self.__name=name # name of the test

#        ##internal data
#        # the different test runs
#        self.__test_runs=[] 
#        # this is the location of the test file
#        self.__test_dir=test_dir
#        #this is the name of the test file
#        self.__test_file=test_file
#        #this is the directory we scanned to find this test
#        self.__test_root=test_root
#        #this is the directory we will run the test in
#        self.__run_dir = os.path.normpath(os.path.join(run_root, name))
#        #this is the result of the test ( did it pass, fail, etc...)
#        self.__result=None

#        ## this is a bit of a hack as this hard coded in.. try to address later
#        # this is the set of extra processes that we might need running 
#        #for the test to work
#        self.__processes=Processes(self)

#        # property objects
#        self.__setup = setup.Setup(self)
#        self.__conditions=conditions.Conditions()
#        # make a copy of the environment so we can modify it without issue
#        self.__env=env
#        #add some default values
#        self.__env['AUTEST_TEST_ROOT_DIR']=self.__test_root
#        self.__env['AUTEST_TEST_DIR']=self.__test_dir
#        self.__env['AUTEST_RUN_DIR']=self.__run_dir
#        # additional variables
#        self.__variables=variables
        
## public properties
#    @property
#    def Name(self):
#        return self.__name

#    @Name.setter
#    def Name(self,val):
#        self.__name=val

#    @property
#    def Summary(self):
#        return self.__summary

#    @Summary.setter
#    def Summary(self,val):
#        self.__summary=val

#    @property
#    def RunSerial(self):
#        return self.__run_serial

#    @RunSerial.setter
#    def RunSerial(self,val):
#        self.__run_serial=val

#    @property
#    def Setup(self):
#        return self.__setup

#    def SkipIf(self,*lst):
#        return self.__conditions._AddConditionIf(lst)

#    def SkipUnless(self,*lst):
#        return self.__conditions._AddConditionUnless(lst)

#    @property
#    def TestDirectory(self):
#        return self.__test_dir

#    @property
#    def TestFile(self):
#        return self.__test_file

#    @property
#    def TestRoot(self):
#        return self.__test_root

#    @property
#    def RunDirectory(self):
#        return self.__run_dir

#    @property
#    def Env(self):
#        return self.__env

#    @Env.setter
#    def Env(self,val):
#        if not is_a.Dict(val):
#            raise TypeError("value needs to be a dict type")
#        self.__env.update(val)

#    @property
#    def Variables(self):
#        return self.__variables

#    @Variables.setter
#    def Variables(self,val):
#        if not is_a.Dict(val):
#            raise TypeError("value needs to be a dict type")
#        self.__variables.update(val)

#    @property
#    def Processes(self):
#        return self.__processes

## public methods 
#    def AddTestRun(self, name='general', displaystr=None):
#        tmp = testrun.TestRun(self, "%s-%s" % (len(self._TestRuns), name), displaystr)
#        self._TestRuns.append(tmp)
#        return tmp
   
#    #internal stuff
#    @property
#    def _Result(self):
#        if self.__result is None:
#            self.__result=self.Processes._TestRun._Result
#            for tr in self.__test_runs:
#                if self.__result < tr._Result:
#                    self.__result = tr._Result
#            # result is None and we have no tests to run
#            if self.__result is None and len(self.__test_runs)==0:
#                return testers.ResultType.Passed
#        return self.__result

#    def _SetResult(self,val):
#        self.__result=val

#    @property
#    def _TestRuns(self):
#        return self.__test_runs

#    @property
#    def _GlobalTestRuns(self):
#        return self.Processes._TestRun

#    @property
#    def _Conditions(self):
#        return self.__conditions

#    #!! not might want to seperate the user interface with the internal logic still with having a 
#    # test_info that is contained within the test object (test info is what we expose...)
    
#    def _run(self):
#        # this is the logic to run the test
#        try:
#            self.doSetup()
#            self.doRun()
#            self.doCleanup()
#        except AttributeError:
#            raise
#        #except SetupError:
#        # setup failed
#        #   self.__test._SetResult(testers.ResultType.)
#        #except RunTestError:
#        # some sort of exception in the running the test
#        #   self.__test._SetResult(testers.ResultType.)
#        #except CleanUpError:
#        # cleanup had some issue
#        #   self.__test._SetResult(testers.ResultType.)
#        # everything else
#        except KeyboardInterrupt:
#            raise
#        except:
#            self.__test._SetResult(testers.ResultType.Exception)
#            self.__test.Setup._Reason = traceback.format_exc()
#            host.WriteVerbose("run_test", "Test {0} failed\n {1}".format(self.__test.Name,self.__test.Setup._Reason))
#            #host.WriteError("run_test", "Test {0} failed\n
#            #{1}".format(self.__test.Name,self.__test.Setup._Reason))
#            return
        

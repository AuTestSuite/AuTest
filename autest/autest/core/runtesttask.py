import autest.glb as glb
from autest.common.task import Task
from autest.common.execfile import execFile
import autest.testers as testers
import hosts.output as host
from autest.common.execfile import execFile
import conditions
from .eventinfo import EventInfo, StartInfo
import autest.common.disk as disk

from exceptions import KeyboardInterrupt
import os
import traceback
import copy
import pprint
import time
import shutil

class RunTestTask(Task):
    def __init__(self, test):
        self.__test=test # this is the test object
        return super(RunTestTask, self).__init__(self)

    def __call__(self):
        # this is the main logic to run a given test
        
        # Make sandbox directory for the given test
        os.makedirs(self.__test.RunDirectory)

        # setup the test for running
        try:
            # read the test file in
            self.readTest()
            
            # check to see that we can run it
            if self.canRunTest:
                # since we passed condition to see if we can run this test
                # go forward with any test setup
                self.setupTest()
                # run it
                self.runTest()
                # clean up any mess
                # such as remove the sandbox if had no issues
                self.cleanupTest()
            else:
                # cannot run test.. report as needed that this being skipped
                reason = self.__test._Conditions._Reason
                host.WriteWarning("Skipping test {0} because:\n {1}".format(self.__test.Name,reason),
                              show_stack=False)
                self.__test._SetResult(testers.ResultType.Skipped)

        except AttributeError:
            raise
        #except SetupError:
        # setup failed
        #   self.__test._SetResult(testers.ResultType.)
        #except RunTestError:
        # some sort of exception in the running the test
        #   self.__test._SetResult(testers.ResultType.)
        #except CleanUpError:
        # cleanup had some issue
        #   self.__test._SetResult(testers.ResultType.)
        # everything else
        except KeyboardInterrupt:
            raise
        except:
            self.__test._SetResult(testers.ResultType.Failed)
            self.__test.Setup._Reason = traceback.format_exc()
            host.WriteVerbose("run_test", "Test {0} failed\n {1}".format(self.__test.Name,self.__test.Setup._Reason))
            #host.WriteError("run_test", "Test {0} failed\n {1}".format(self.__test.Name,self.__test.Setup._Reason))
            return
        
#        except:
#            self.__test._SetResult(testers.ResultType.Failed)


    @property
    def canRunTest(self):
        if not self.__test._Conditions._Passed:
            return False
        return True

    def setupTest(self):
        host.WriteVerbosef("run_test","Setting Test {0}",self.__test)
        self.__test.Setup._do_setup()

    def cleanupTest(self):
        host.WriteVerbosef("run_test","Cleanup Test {0}",self.__test)
        #need to add a cleanup phase
        
        # clean up an processes that might stil be running

        self.stopGlobalProcess()
        #if test passed as we don't want to keep the tests
        # we can remove it
        if self.__test._Result == testers.ResultType.Passed:
            shutil.rmtree(self.__test.RunDirectory, onerror=disk.remove_read_only)

    def readTest(self):
        #First we need to load a given test
        #host.WriteMessage('Reading Test infomation "{0}" in
        #{1}'.format(self.__test.Name,self.__test.TestDirectory))

        # load the test data.  this mean exec the data
        #create the locals we want to pass
        locals = copy.copy(glb.Locals)

        locals.update({
                'test': self.__test, #backwards compat
                'Test': self.__test,
                'Setup': self.__test.Setup,
                'Condition': conditions.ConditionFactory(),
                'Testers': testers,
                })

        #get full path
        fileName = os.path.join(self.__test.TestDirectory, self.__test.TestFile)
        execFile(fileName,locals,locals)
        host.WriteVerbose("reading",'Done reading test "{0}"'.format(self.__test.Name))

    def runTest(self):
        # this will run a given test.
        # it will go through the different "test runs" or steps
        skip_tests = None
        host.WriteMessagef("Running Test {0}:",self.__test.Name,end="")
        for tr in self.__test._TestRuns:
            if skip_tests:
                # we had some failure so we are skipping the rest of the tests runs
                tr._Result = testers.ResultType.Skipped
            else:
                #run the test step
                try:
                    # dump out events that have been registered for debugging
                    host.WriteDebugf("testrun","Registered events for test run {0}:\n {1}",tr.Name, pprint.pformat(tr._GetRegisteredEvents()))
                    # bind the events now
                    tr._RegisterEvent("runtest", tr.StartEvent, self.runTestStep)
                    tr._BindEvents()
                    # run events
                    tr.SetupEvent(EventInfo())
                    tr.StartEvent(StartInfo(tr))
                    tr.EndEvent(EventInfo())
                except KeyboardInterrupt:
                    raise
                except:
                    # something went wrong..
                    tr._Result = testers.ResultType.Exception
                    tr._ExceptionMessage = traceback.format_exc()
            
                    # todo add logic to continue if test had failed in set to allow for this.
            if tr._Result == testers.ResultType.Failed:
                host.WriteMessagef("F",end="")
                host.WriteVerbose("run_test",
                                  'Stopping test run for test "{0}" because test run "{1}" failed'.format(
                                               self.__test.Name,
                                               tr.Name
                                               )
                                  )
                skip_tests = tr.Name
            elif tr._Result == testers.ResultType.Exception:
                host.WriteWarning('Stopping test run for test "{0}" because test run "{1}" had an Exception:\n {2}'.format(
                                               self.__test.Name,
                                               tr.Name,
                                               tr._ExceptionMessage
                                               )
                                  )
                skip_tests = tr.Name
            else:
                host.WriteMessagef(".",end="")
                
        host.WriteMessage("")

    def _gen_process_list(self,tr):
        def append_not_exist(olst,nlst):
            for l in nlst:
                if l not in olst:
                    olst.append(l)
                    
        def getlst(lst,stack):
            ret=[]
            for l in lst:
                # break any loops
                if l in stack:
                    continue
                stack.append(l)
                ret.extend(getlst(l.StartBefore,stack))
                ret.append(l)
                ret.extend(getlst(l.StartAfter,stack))
            return ret
        
        fat_lst=[]
        ret=[]
        d=tr.Processes.Default
        fat_lst.extend(getlst(d.StartBefore,[d]))
        fat_lst.append(d)
        fat_lst.extend(getlst(d.StartAfter,[d]))
        
        append_not_exist(ret,fat_lst)

        return ret


    def runTestStep(self,ev):
        # get the processes we need to run in order
        tr=ev.TestRun
        ps=self._gen_process_list(tr)
        # run each process
        for p in ps:
            p._Start()
        # wait for default process stop
        while tr.Processes.Default._isRunning():
            for p in ps:
                p._Poll()

        # check for all processes to end with a time frame
        st=time.time()
        while 1:
            running=None
            for p in ps:
                # Check to see that it is in the global process list
                # if it is not in the lists we will try to shut it down
                # this allows for process to be from different test runs
                # to be used in this test run.. hwoever that is OK I think..
                if p not in tr._Test.Processes._GetProcesses() and p._Poll():
                    running=p
            
            if running:
                running._wait(1)
            else:
                # everything finished
                break
            #if the time we will wait up?
            if time.time() - st > 15.0: 
                # we kill them
                for p in ps:
                    if p._isRunning():
                        p._kill()
                break
    
    def stopGlobalProcess(self):  
        st=time.time()
        ps = self.__test.Processes._GetProcesses()
        while len(ps):
            running=None
            for p in ps:
                # Check to see that it is in the global process list
                # if it is not in the lists we will try to shut it down
                # this allows for process to be from different test runs
                # to be used in this test run.. hwoever that is OK I think..
                if p._Poll():
                    running=p
            if running:
                running._wait(1)
            else:
                # everything finished
                break
            #if the time we will wait up?
            if time.time() - st > 5.0: 
                # we kill them
                for p in ps:
                    if p._isRunning():
                        p._kill()
                break

    
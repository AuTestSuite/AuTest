from __future__ import absolute_import, division, print_function
import autest.glb as glb
from autest.common.task import Task
from autest.common.execfile import execFile
import autest.testers as testers
import hosts.output as host
from autest.common.execfile import execFile
from . import conditions
from .eventinfo import EventInfo, StartInfo
import autest.common.disk as disk
from autest.exceptions.killonfailure import KillOnFailureError

import os
import traceback
import copy
import time
import shutil
from collections import namedtuple

class RunTestTask(Task):
    def __init__( self, test ):
        self.__test = test # this is the test object
        return super(RunTestTask, self).__init__(self)

    def __call__( self ):
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
                # cannot run test..  report as needed that this being skipped
                reason = self.__test._Conditions._Reason
                host.WriteWarning("Skipping test {0} because:\n {1}".format(self.__test.Name,reason),
                              show_stack=False)
                self.__test._SetResult(testers.ResultType.Skipped)

                # clean up any mess
                # such as remove the sandbox if had no issues
                self.cleanupTest()

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
            self.__test._SetResult(testers.ResultType.Exception)
            self.__test.Setup._Reason = traceback.format_exc()
            host.WriteVerbose("run_test", "Test {0} failed\n {1}".format(self.__test.Name,self.__test.Setup._Reason))
            #host.WriteError("run_test", "Test {0} failed\n
            #{1}".format(self.__test.Name,self.__test.Setup._Reason))
            return
        
#        except:
#            self.__test._SetResult(testers.ResultType.Failed)


    @property
    def canRunTest( self ):
        if not self.__test._Conditions._Passed:
            return False
        return True

    def setupTest( self ):
        host.WriteVerbosef("run_test","Setting Test {0}",self.__test)
        self.__test.Setup._do_setup()

    def cleanupTest( self ):
        host.WriteVerbosef("run_test","Cleanup Test {0}",self.__test)
        #need to add a cleanup phase
        
        # clean up an processes that might stil be running
        try:
            self.stopGlobalProcess()
        
            #if test passed as we don't want to keep the tests
            # we can remove it
            if self.__test._Result == testers.ResultType.Passed or self.__test._Result == testers.ResultType.Skipped:
                shutil.rmtree(self.__test.RunDirectory, onerror=disk.remove_read_only)
        except KeyboardInterrupt:
            host.WriteMessage("Control-C detected! Shutting down tests processes")
            self.hardStopProcess(self.__test.Processes._GetProcesses())
            host.WriteMessage("Processes have been shutdown!")
            raise

    def readTest( self ):
        # load the test data.  this mean exec the data
        #create the locals we want to pass
        locals = copy.copy(glb.Locals)

        locals.update({
                'test': self.__test, #backwards compat
                'Test': self.__test,
                'Setup': self.__test.Setup,
                'Condition': conditions.ConditionFactory(),
                'Testers': testers,
                # break these out of tester space
                # to make it easier to right a test
                'Any':testers.Any,
                'All':testers.All,
                'Not':testers.Not,
                'When':glb.When(),
                })

        #get full path
        fileName = os.path.join(self.__test.TestDirectory, self.__test.TestFile)
        execFile(fileName,locals,locals)
        host.WriteVerbose("reading",'Done reading test "{0}"'.format(self.__test.Name))

    def runTest( self ):
        # this will run a given test.
        # it will go through the different "test runs" or steps
        skip_tests = None
        host.WriteMessagef("Running Test {0}:",self.__test.Name,end="")
        # dump out events that have been registered for debugging
        host.WriteDebugf("testrun","Registered events for test run {0}:\n {1}",self.__test.Processes._TestRun.Name, self.__test.Processes._TestRun.dump_event_data())
        self.__test.Processes._TestRun._BindEvents()
        for tr in self.__test._TestRuns:
            if skip_tests:
                # we had some failure so we are skipping the rest of the tests runs
                tr._Result = testers.ResultType.Skipped
            else:
                #run the test step
                try:
                    # dump out events that have been registered for debugging
                    host.WriteDebugf("testrun","Registered events for test run {0}:\n {1}",tr.Name, tr.dump_event_data())

                    # bind the events now
                    tr._RegisterEvent("runtest", tr.StartEvent, 
                        testers.Lambda(self.runTestStep))
                    tr._BindEvents()
                    # run events
                    tr.SetupEvent(EventInfo())
                    tr.StartEvent(StartInfo(tr))
                    tr.EndEvent(EventInfo())
                except KeyboardInterrupt:
                    host.WriteMessage("Control-C detected! Shutting down tests processes")
                    ps = self._gen_process_list(tr)
                    self.stopProcess(ps)
                    self.hardStopProcess(self.__test.Processes._GetProcesses())
                    host.WriteMessage("Processes have been shutdown!")
                    raise
                except:
                    # something went wrong..
                    tr._Result = testers.ResultType.Exception
                    tr._ExceptionMessage = traceback.format_exc()
            
                    # todo add logic to continue if test had failed in set to allow for this.
            if tr._Result == testers.ResultType.Failed:
                host.WriteMessagef("F",end="")
                host.WriteVerbose("run_test",
                                  'Stopping test run for test "{0}" because test run "{1}" failed'.format(self.__test.Name,
                                               tr.Name))
                skip_tests = tr.Name
            elif tr._Result == testers.ResultType.Exception:
                host.WriteWarning('Stopping test run for test "{0}" because test run "{1}" had an Exception:\n {2}'.format(self.__test.Name,
                                               tr.Name,
                                               tr._ExceptionMessage))
                skip_tests = tr.Name
            else:
                host.WriteMessagef(".",end="")
                
        host.WriteMessage("")

    def _gen_process_list( self,tr ):
        PD = namedtuple("process_data","process readyfunc args")        
                
        def append_not_exist( olst,nlst ):
            for l in nlst:
                if l not in olst:
                    olst.append(l)
        
        def getlst( data,stack,default_proc ):
            ret = []
            
            for proc,func_info in data.items():
                info = PD(proc,func_info[0],func_info[1])
                # break any loops
                if info in stack:
                    host.WriteMessagef("Ignoring adding {0} to start order as it is already exist, breaking loop.",info)
                    continue
                #will pass in default process
                #if default in stack:
                #    host.WriteMessagef("Ignoring adding {0} to start order as it is already exist,
                #    breaking loop.",info)
                #    continue
                stack.append(info)
                ret.extend(getlst(proc.StartBefore(),stack, default_proc))
                ret.append(info)
                ret.extend(getlst(proc.StartAfter(),stack, default_proc))
            return ret
        
        fat_lst = []
        ret = []
        d = tr.Processes.Default
        fat_lst.extend(getlst(d.StartBefore(),[],d))
        fat_lst.append(PD(d,d._isReady,{}))
        fat_lst.extend(getlst(d.StartAfter(),[],d))
        
        #append_not_exist(ret,fat_lst)

        return fat_lst


    def __start_process( self,ps ):
        try:
            # note a given process might be in the list more than once
            # this mean there are different requirements for the next process
            # to be considered ready we want to test for
            for idx,p in enumerate(ps):
                # get next process if any as we will want to
                # use this process name to help with error messages
                # for the user
                try:
                    next_process = ps[idx + 1].process
                except IndexError:
                    # we are at the last process or we only have one process to start
                    # In either case we don't need to wait
                    # for process to be ready
                    # Start the process and continue
                    p.process._Start()                    
                    break
                # if we are here we have more than one process
                # we need to start and want to wait on being ready
                # and we are not at the end of the list.
                p.process._waitingProcess = next_process.Name
                #if already started, it will just return
                p.process._Start()
                
                # Start timer as we have something
                # we have to wait on, and we need to make
                # sure we have a fallback if something is wrong with
                # the isReady logic never becoming ready in time
                p.process._startReadyTimer()
                isReady = False
                while not isReady:
                    try:
                        isReady = p.readyfunc(**p.args)
                    except TypeError:
                        isReady = p.readyfunc()
                    # if it is ready set state on process
                    if isReady:
                        p.process._stopReadyTimer()
                        p.process._waitingProcess = None
                        continue
                    # verify we are running...
                    if not p.process._isRunning():
                        #
                        self.stopProcess(ps)
                        self.stopGlobalProcess()
                        return True, 'Waiting for process "{0}" to become ready'.format(p.process.Name), 'Process finished before it was ready'
                    # test that the process started in the time needed
                    if p.process.StartupTimeout < p.process._readyTime(time.time()):
                        self.stopProcess(ps)
                        self.stopGlobalProcess()
                        return (True, 
                                "Checking that process is ready within {0} seconds so we can start process: {1}".format(p.process.StartupTimeout,next_process.Name),
                                "Process failed to become ready in time")
                    # poll other processes
                    for op in ps:
                        
                        if op.process._isRunning():
                            try:
                                # Need to do poll on running processes to make sure any events or test run correctly
                                # while we start up the set of processes
                                op.process._Poll()
                            except KillOnFailureError:
                                self.stopProcess(ps)
                                self.stopGlobalProcess()
                                return (True, 'Waiting for process "{0}" to become ready'.format(p.process.Name), "Test run stopped because Kill On Failure")
        except KillOnFailureError as e:
            self.stopProcess(ps)
            self.stopGlobalProcess()
            return (True, 'Starting process {0}'.format(p.process.Name), e.info)

    def runTestStep( self,ev ):
        # get the processes we need to run in order
        tr = ev.TestRun
        ps = self._gen_process_list(tr)
        # run each process
        ret = self.__start_process(ps)
        if ret is not None:
           return ret
        
        # wait for default process stop
        while tr.Processes.Default._isRunning():
            for p in ps:
                try:
                    p.process._Poll()
                except KillOnFailureError:
                    self.stopProcess(ps)
                    self.stopGlobalProcess()
                    return (True, 'Waiting for "Default" process to finish', "Test run stopped because Kill On Failure")
                time.sleep(.1)
        # check for all processes to end with a time frame
        st = time.time()
        while 1:
            running = None
            for p in ps:
                # Check to see that it is in the global process list
                # if it is not in the lists we will try to shut it down
                # this allows for process to be from different test runs
                # to be used in this test run..  hwoever that is OK I think..
                if p.process not in tr._Test.Processes._GetProcesses() and p.process._Poll():
                    running = p.process
            
            if running:
                running._wait(1)
            else:
                # everything finished
                break
            #if the time we will wait up?
            if time.time() - st > 15.0: 
                # we kill them
                self.stopProcess(ps)
                break
        return False,"Running all process for TestRun","All processes ran"
    
    def stopProcess( self,ps ):
        self.hardStopProcess([p.process for p in ps ])        

    def hardStopProcess( self,ps ):
         for p in ps:
            if p._isRunning():
                p._kill()

    def stopGlobalProcess( self ):  
        st = time.time()
        ps = self.__test.Processes._GetProcesses()
        while len(ps):
            running = None
            for p in ps:
                # Check to see that it is in the global process list
                # if it is not in the lists we will try to shut it down
                # this allows for process to be from different test runs
                # to be used in this test run..  hwoever that is OK I think..
                if p._Poll():
                    running = p
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

    
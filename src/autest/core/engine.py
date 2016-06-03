from __future__ import absolute_import, division, print_function
import autest.glb as glb
import autest.common.execfile as execfile
import hosts.output as host
import autest.api as api
from . import setupitem
from . import runtesttask
import autest.testers.tester as testers
from autest.common.disk import remove_read_only
from . import report 
from . import test


import os
from fnmatch import fnmatch
import time
import shutil



class Engine(object):
    """description of class"""

    def __init__(self, jobs=1, test_dir='./', run_dir="./_sandbox", autest_site=None,
                 filters='*', dump_report=False, env=None):

        self.__tests = {}  # the dict of the different tests we have {name:testobj}
        self.__jobs = jobs  # how many jobs to try to run at a given time
        self.__test_dir = test_dir  # this the root directory to look for the tests
        self.__run_dir = os.path.abspath(run_dir) # this is the directory to run the tests in
        self.__autest_site = autest_site # any special autest directory to look up.  None uses standard one
        self.__filters = filters  # which set of tests to run        
        self.__ENV = env

        # setup the thread poool to run all the tasks
        #if jobs > 1:
            #self.__pool = ThreadPool(jobs)
        
        #set the engine to be easy to access
        if glb.Engine:
            raise RuntimeError("Only one engine can be created at a time")
        glb.Engine = self
       

    def Start(self):

        #load setup items
        import autest.setupitems
        #load testrun items
        import autest.testrunitems

        #self.__timer.startEvent('total')
        if os.path.exists(self.__run_dir):
            #self.__timer.startEvent('sandbox cleanup')
            host.WriteVerbose("engine", "The Sandbox directory exists, will try to remove")
            oldExceptionArgs = None
            while True:
                try:
                    shutil.rmtree(self.__run_dir, onerror=remove_read_only)
                except BaseException as e:
                    if e.args != oldExceptionArgs:
                        # maybe this is Windows issue where antivirus won't let
                        # us remove
                        # some random directory, so we're waiting & retrying
                        oldExceptionArgs = e.args
                        time.sleep(1)
                        continue
                    host.WriteError(("Unable to remove sandbox directory for clean test run" + \
                                     "\n Reason: {0}").format(e), show_stack=False)
                    raise
                else:
                    # no exceptions, the directory was wiped
                    break
            host.WriteVerbose("engine", "The Sandbox directory was removed")
            #self.__timer.stopEvent('sandbox cleanup')
        #self.__timer.startEvent('extensions load')
        host.WriteVerbose("engine", "Loading Extensions")
        self._load_extensions()
        #self.__timer.stopEvent('extensions load')
        #self.__timer.startEvent('scanning for tests')
        host.WriteVerbose("engine", "Scanning for tests")
        self._scan_for_tests()
        if not self.__tests:
            host.WriteMessage("No tests found to run")
            host.WriteMessage("If your tests are in a different directory try using --directory=<path with tests>")
            return ""
        #self.__timer.stopEvent('scanning for tests')
        host.WriteVerbose("engine", "Running tests")
        self._run_tests()
        #self.__timer.startEvent('making report')
        host.WriteVerbose("engine", "Making report")
        result = self._make_report()
        #self.__timer.stopEvent('making report')
        #self.__timer.stopEvent('total')
        #for eventName, eventDuration in self.__timer.getEvents():
            #print 'durations', '%s - %.2f sec.' % (eventName.ljust(40),
            #eventDuration)
            #host.WriteVerbose('durations', '%s - %.2f sec.' %
            #(eventName.ljust(40), eventDuration))
        return result

    def _load_extensions(self):
        # load files of our extension type in the directory

        # add expected API function so they can be called
        locals = {
                'AddTestRunSet':api.ExtendTest, 
                'AddSetupTask':api.AddSetupItem, # backward compat
                'AddSetupItem':api.AddSetupItem,
                'SetupTask':setupitem.SetupItem, # backward compat
                'SetupItem':setupitem.SetupItem,
                'AddTestRunMember':api.AddTestRunMember,
                'AddWhenFunction':api.AddWhenFunction,
                }


        # Which directory to use
        if self.__autest_site is None:
            # this is the default
            path = os.path.join(self.__test_dir,'autest-site')
        else:
            #This is a custom location
            path = os.path.abspath(self.__autest_site)

        # given it exists we want to load data from it
        if os.path.exists(path):
            host.WriteVerbose("engine","Loading Extensions from {0}".format(path))
            for f in os.listdir(path):
                f = os.path.join(path,f)
                if os.path.isfile(f) and f.endswith("test.ext"):
                    execfile.execFile(f,locals,locals)
        elif self.__autest_site is not None:
            host.WriteError("Custom autest-site path note found. Looking for:\n {0}".format(path))
        else:
            host.WriteVerbose("engine","autest-site path not found")

    def _scan_for_tests(self):
        # scan for tests in and under the provided test directory
        for root, dirs, files in os.walk(self.__test_dir):
            host.WriteVerbose("test_scan","Looking for tests in",root)
            # Note because we are using os.walk we get the file name with our
            # directory
            # this mean we have to check for duplicated in names else we will
            # have conflicts
            # ie a test might not run as it was replaced by a test with the
            # same name that
            # was loaded at a later time.
            for f in files:
                if f.endswith('.test.py') or f.endswith(".test"):
                    if f.endswith('.test.py'):
                        name = f[:-len('.test.py')]
                    else:
                        name = f[:-len('.test')]
                    match = False
                    for filter in self.__filters:
                        if not filter.startswith("*"):
                            filter = "*" + filter
                        if fnmatch(os.path.join(root,name), filter):
                            # we have a match, use this test
                            break
                    else:
                        # did not get a match
                        host.WriteVerbose("test_scan","   Skipping test",name)
                        continue
                    if name in self.__tests:
                        host.WriteWarning("overiding test",name, "with test in", root)
                    host.WriteVerbose("test_scan","   Found test",name)
                    self.__tests[name] = test.Test(name,root,f,self.__run_dir,self.__test_dir,self.__ENV)

    def _run_tests(self):
        if self.__jobs > 1:
            for t in self.__tests.values():
                self.__pool.addTask(self.__run_test_task, t)
            self.__pool.waitCompletion()
        else:
            for t in self.__tests.values():
                self.__run_test_task(t)

    def __run_test_task(self, task):
        #self.__timer.startEvent('running test <{0}>'.format(task.Name))
        runtesttask.RunTestTask(task)()
        #self.__timer.stopEvent('running test <{0}>'.format(task.Name))

    def _make_report(self):
        # need to clean this up more...
        reportdata = report.TestsReport()
        for test in self.__tests.values():
            reportdata.addTestRun(test)
        host.WriteMessage("\nReport: --------------")
        for msg in reportdata.exportForConsole():
            host.WriteMessage(msg)
        host.WriteMessage("")
        if sum([reportdata.stats[resType] for resType in (testers.ResultType.Exception,
                                                      testers.ResultType.Failed,
                                                      testers.ResultType.Unknown,
                                                      testers.ResultType.Warning)]) > 0:
            host.WriteMessage('Test run had issues!')
            runResult = 1
        else:
            host.WriteMessage('All tests passed')
            runResult = 0
        for resType in (testers.ResultType.Unknown, testers.ResultType.Exception,
                        testers.ResultType.Failed,  testers.ResultType.Warning,
                        testers.ResultType.Skipped, testers.ResultType.Passed):
            amount = reportdata.stats[resType]
            host.WriteMessage(' {0}: {1}'.format(testers.ResultType.to_string(resType), amount))

        #if self.__dump_report:
            #host.WriteMessage('\n\n{JSON_REPORT}%s{/JSON_REPORT}' %
            #reportdata.exportForJson())
        return runResult

    @property
    def Host(self):
        return self.__host
'''
Report object that knows how to print itself and can be exported to a file
'''
from __future__ import absolute_import, division, print_function
from autest.testers.tester import ResultType, Tester
import hosts.output as host
import colorama
import collections
import json
import abc

class ReportInfo(object):
    ''' class contains information about the tests stats
        and accessors to get the test based on there status
    '''

    def __init__(self, tests):
        #counts...
        self.__stats={
                0:0, # Unknown =0
                1:0, # Passed = 1
                2:0, # Skipped = 2
                3:0, # Warning = 3
                4:0, # Failed = 4    
                5:0, # Exception = 5
        }
        # the tests group by there status
        self.__grouped_tests={
                        100:[] # clean up key.. value is all not passing tests
                        }
        self.__tests=tests

        for t in tests:
            self.__stats[t._Result]+=1
            try:
                self.__grouped_tests[t._Result].append(t)
            except KeyError:
                self.__grouped_tests[t._Result]=[t]
            
            if t._Result in [ResultType.Exception,ResultType.Failed,ResultType.Unknown]:
                self.__grouped_tests[100].append(t)

    @property
    def stats(self):
        return self.__stats
    @property
    def Unknown(self):
        return self.__grouped_tests.get(ResultType.Unknown,[])
    @property
    def Passed(self):
        return self.__grouped_tests.get(ResultType.Passed,[])
    @property
    def Skipped(self):
        return self.__grouped_tests.get(ResultType.Skipped,[])
    @property
    def Warning(self):
        return self.__grouped_tests.get(ResultType.Warning,[])
    @property
    def Failed(self):
        return self.__grouped_tests.get(ResultType.Failed,[])
    @property
    def Exception(self):
        return self.__grouped_tests.get(ResultType.Exception,[])
    @property
    def NotPassing(self):
        # all tests that are not skipped, warning or passing
        return self.__grouped_tests.get(100,[])
    @property
    def Tests(self):
        return self.__tests


def GenerateReport(info,):#args):
    '''default ConsoleHost based reprot'''
    
    def TestRunInfo(tr):
        return " {0}: {2}{1}{3}".format(tr.DisplayString,ResultType.to_string(tr._Result),colorama.Style.BRIGHT,colorama.Style.NORMAL)

    def TestInfo(test):
        return 'Test "{0}" {3}\n    File: {1}\n    Directory: {2}'.format(test.Name,test.TestFile,test.TestDirectory,ResultType.to_string(test._Result))

    def CheckerInfo(check,indent=0):
        ret=""
        if check.Result == ResultType.Passed:
            reason = None
        else:
            reason = check.Reason
        result=ResultType.to_string(check.Result)
        ret= '{3}  {0} : {1} - {2}\n'.format("For {0}".format(check.DescriptionGroup) if check.DescriptionGroup is not None else "checking", check.Description, result," "*indent)
        ret+='{1}    Reason: {0}'.format(check.Reason," "*indent)
        if check.isContainer:
            for tester in check._testers:
                ret+="\n"
                ret+=CheckerInfo(tester,indent+4)
        return ret

    # report an skipped tests
    if True:#args.report_skipped:
        skipped=info.Skipped

        print("{0} Tests were skipped:".format(len(skipped)))
        print("-"*80)
        for test in skipped:
            print(' Test "{0}" Skipped\n    File: {1}\n    Directory: {2}'.format(test.Name,test.TestFile,test.TestDirectory))
            print("  Reason: {0}".format(test._Conditions._Reason))
            print()

    # report tests that only had warnings
    if len(info.Warning):
        print("{0} Tests had warnings:".format(len(skipped)))
        #for test in info.Warning:
            
    #report tests that had issues (unkown, failed, exceptions)
    tests=info.NotPassing
    for test in tests:
        # report about the test as a whole
        print(TestInfo(test))
        #Format the information about the test run
        for tr in test._TestRuns + [test._GlobalTestRuns]:
            # information about the given test run
            print(TestRunInfo(tr))
            if tr._Result == ResultType.Passed:
                #runMessage = (self.ITEM_PASS, None)
                pass
            elif tr._Result == ResultType.Skipped:
                print("  Previous test run failed")
            elif tr._Result == ResultType.Exception and tr._ExceptionMessage:
                print(tr._ExceptionMessage)    
            else:
                # dump information about the checks we did for the test run
                for check in tr._getTesters():
                    if check.RanOnce:
                        print(CheckerInfo(check))
            print()
    for resType in (ResultType.Unknown, ResultType.Exception,
                        ResultType.Failed, ResultType.Warning,
                        ResultType.Skipped, ResultType.Passed):
            amount = info.stats[resType]
            host.WriteMessage(' {0}: {1}'.format(ResultType.to_string(resType), amount))
           
    



#class TestsReport(object):
#    ITEM_PASS =    'passed'
#    ITEM_SKIPPED = 'skipped'
#    ITEM_NOTRUN =  'not run'
#    ITEM_OTHER =   'other'

#    def __init__(self):
#        self.testRuns = {}
#        self.stats = collections.defaultdict(int)

#    def addTestRun(self, test):
#        if test._Result == ResultType.Skipped:
#            message = (self.ITEM_SKIPPED, str(test._Conditions._Reason))
#        elif test._Result == ResultType.Passed:
#            message = (self.ITEM_PASS, None)
#        elif test.Setup._Failed:
#            message = (self.ITEM_NOTRUN, str(test.Setup._Reason))
#        else:
#            runs = []
#            for tr in test._TestRuns +[test._GlobalTestRuns]:
#                if tr._Result == ResultType.Passed:
#                    runMessage = (self.ITEM_PASS, None)
#                elif tr._Result == ResultType.Skipped:
#                    runMessage = (self.ITEM_SKIPPED, 'previous test run failed.')
#                elif tr._Result == ResultType.Exception and tr._ExceptionMessage:
#                    runMessage = (self.ITEM_NOTRUN, tr._ExceptionMessage)
#                else:
#                    checkers = []
#                    for check in tr._getTesters():
#                        if not check.UseInReport:
#                            continue
#                        if check.Result == ResultType.Passed:
#                            reason = None
#                        else:
#                            reason = str(check.Reason)
#                        checkers.append((
#                                        check.DescriptionGroup, 
#                                        check.Description, 
#                                        ResultType.to_string(check.Result),
#                                        reason, 
#                                        False))
#                    runMessage = (self.ITEM_OTHER, checkers)
#                runs.append((tr.Name, ResultType.to_string(tr._Result)) + runMessage)
#            message = (self.ITEM_OTHER, runs)
#        self.testRuns[(test.TestDirectory, test.TestFile)] = message
#        self.stats[test._Result] += 1

#    def _asStrList(self, testDir, testFile, addStreamBoth=False):
#        status, message = self.testRuns[(testDir, testFile)]

#        if status != self.ITEM_PASS:
#            yield '\nTest run "{0}" in directory "{1}"'.format(testFile, testDir)
#            if status == self.ITEM_SKIPPED:
#                yield '  Skipped: %s' % message
#            elif status == self.ITEM_NOTRUN:
#                yield '  Setup failed: %s' % message
#            else:
#                for runName, statusStr, runStatus, runMessage in message:
#                    yield '\n  %s: %s' % (runName, statusStr)
#                    if runStatus != self.ITEM_OTHER:
#                        if runMessage:
#                            yield '    Reason: %s' % runMessage
#                    else:
#                        for des_grp, description, result, reason, streamBoth in runMessage:
#                            if streamBoth and not addStreamBoth:
#                                continue
#                            yield '    {0} : {1} - {2}'.format("For {0}".format(des_grp) if des_grp is not None else "checking", description, result)
#                            if reason:
#                                yield '      Reason: %s' % reason

#    def exportForConsole(self):
#        for testDir, testFile in self.testRuns.keys():
#            for msg in self._asStrList(testDir, testFile):
#                yield msg

#    def exportForJson(self):
#        result = []
#        for (testDir, testFile), (status, msg) in self.testRuns.items():
#            messages = [msg for msg in self._asStrList(testDir, testFile, addStreamBoth=True)]
#            result.append((testDir, testFile, status, '\n'.join(messages)))
#        return json.dumps(result)


from __future__ import absolute_import, division, print_function
from autest.testers.tester import ResultType, Tester
import hosts.output as host


def GenerateReport(info,):#args):
    '''default ConsoleHost based reprot'''
    
    def TestRunInfo(tr):
        return " {0}: {1}".format(tr.DisplayString,ResultType.to_color_string(tr._Result))

    def TestInfo(test):
        return 'Test "{0}" {3}\n    File: {1}\n    Directory: {2}'.format(test.Name,test.TestFile,test.TestDirectory,ResultType.to_color_string(test._Result))

    def CheckerInfo(check,indent=0):
        ret=""
        if check.Result == ResultType.Passed:
            reason = None
        else:
            reason = check.Reason
        result=ResultType.to_color_string(check.Result)
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

import autest.api as api

api.RegisterReporter(GenerateReport,name="default")
api.RegisterReporter(GenerateReport,name="color-console")

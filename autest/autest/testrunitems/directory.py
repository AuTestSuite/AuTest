from __future__ import absolute_import, division, print_function
import autest.core.testrunitem as testrunitem
import autest.testers as testers

import os

class Directory(testrunitem.TestRunItem):
    '''
    Allows us to test for a file. We can test for existance
    '''
    def __init__(self, testrun, name, exists = True, runtime=True):
        super(Directory, self).__init__(testrun)
        self.__name = name
        self.__runtime=runtime
        if exists:
            self.Exists = exists

    def __str__(self):
        return self.Name

    def GetContent(self, eventinfo):
        return self.AbsPath, ""

    @property
    def AbsPath(self):
        '''
        The absolute path of the file, runtime value
        '''
        if self.__runtime:
            return self.AbsRunTimePath
        return self.AbsTestPath

    @property
    def AbsRunTimePath(self):
        '''
        The absolute path of the file, based on Runtime sandbox location
        '''
        return os.path.normpath(os.path.join(self._TestRun._Test.RunDirectory, self.Name))

    @property
    def AbsTestPath(self):
        '''
        The absolute path of the file, based on directory relative form the test file location
        '''
        return os.path.normpath(os.path.join(self._TestRun._Test.TestDirectory, self.Name))

    @property
    def Name(self):
        return self.__name

    @Name.setter
    def Name(self, val):
        self.__name = val

    @property
    def Exists(self):
        return self._GetRegisterEvent("Directory.{0}.Exists".format(self.__name))

    @Exists.setter
    def Exists(self, val):
        def getChecker():
            if isinstance(val, testers.Tester):
                val.TestValue = self
                return val
            elif val == True:
                return testers.DirectoryExists(True, self)
            elif val == False:
                return testers.DirectoryExists(False, self)
        self._Register('Directory.{0}.Exists'.format(self.__name), getChecker,self._TestRun.EndEvent)

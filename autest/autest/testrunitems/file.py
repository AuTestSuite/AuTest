import autest.core.testrunitem as testrunitem
import autest.testers as testers
import os 

class File(testrunitem.TestRunItem):
    '''
    Allows us to test for a file. We can test for size, existance and content
    '''
    def __init__(self, testrun, name, exists = None, size = None, content_tester = None,execute=False,runtime=True):
        super(File, self).__init__(testrun)
        self.__name = name
        self.__runtime=runtime
        if exists:
            self.Exists = exists
        if size:
            self.Size = size
        if content_tester:
            self.Content = content_tester
        if execute:
            self.Execute = execute

    def __str__(self):
        return self.Name

    def GetContent(self,eventinfo):
        return self.AbsPath,""

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
        return self._GetRegisterEvent("File.{0}.Exists".format(self.__name))

    @Exists.setter
    def Exists(self, val):
        def getChecker():
            if isinstance(val, testers.Tester):
                val.TestValue = self
                return val
            elif val == True:
                return testers.FileExists(True, self)
            elif val == False:
                return testers.FileExists(False, self)
        self._Register("File.{0}.Exists".format(self.__name), getChecker,self._TestRun.EndEvent)

    def GetSize(self):
        statinfo = os.stat(self.AbsPath)
        return statinfo.st_size

    @property
    def Size(self):
        return self._GetRegisterEvent("File.{0}.Size".format(self.__name))

    @Size.setter
    def Size(self, val):
        def getChecker():
            if isinstance(val, testers.Tester):
                val.TestValue = self
                return val
            else:
                return testers.Equal(int(val), test_value=self.GetSize)
        self._Register("File.{0}.Size".format(self.__name), getChecker,self._TestRun.EndEvent)

    @property
    def Content(self):
        return self._GetRegisterEvent("File.{0}.Content".format(self.__name))

    @Content.setter
    def Content(self, val):
        def getChecker():
            if isinstance(val, testers.Tester):
                val.TestValue = self
                return val
            elif isinstance(val, basestring):
                return testers.GoldFile(File(self._TestRun, val, runtime=False),
                                        test_value=self)
            elif isinstance(val, (tuple, list)):
                return testers.GoldFileList([File(self._TestRun, item, runtime=False)
                                             for item in val], test_value=self)

        self._Register("File.{0}.Content".format(self.__name), getChecker,self._TestRun.EndEvent)

    @property
    def Executes(self):
        return self._GetRegisterEvent("File.{0}.Execute".format(self.__name))

    @Executes.setter
    def Executes(self, val):
        def getChecker():
            if isinstance(val, testers.Tester):
                val.TestValue = self
                return val
            elif val == True:
                return testers.RunFile(True, self)
            elif val == False:
                return testers.RunFile(False, self)
            else:
                return testers.RunFile(val, self)
        self._Register("File.{0}.Execute".format(self.__name), getChecker,self._TestRun.EndEvent)

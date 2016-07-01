from __future__ import absolute_import, division, print_function
import autest.core.testrunitem as testrunitem
from autest.core.testerset import TesterSet
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
        
        # setup testables
        des_grp="{0} {1}".format("file",self.__name)
        # exists
        self._Register(
            "File.{0}.Exists".format(self.__name),
            TesterSet(
                    testers.FileExists,
                    self,
                    self._TestRun.EndEvent,
                    converter=bool,
                    description_group=des_grp
                ),"Exists"
            )
        # size 
        self._Register(
            "File.{0}.Size".format(self.__name),
            TesterSet(
                    testers.Equal,
                    self.GetSize,
                    self._TestRun.EndEvent,
                    converter=int,
                    description_group=des_grp,
                    description="File size is {0.Value} bytes"
                ),"Size"
            )
        # content
        self._Register(
            "File.{0}.Content".format(self.__name),
            TesterSet(
                    testers.GoldFile,
                    self,
                    self._TestRun.EndEvent,
                    converter=lambda x: File(self._TestRun, x, runtime=False),
                    description_group=des_grp
                ),"Content"
            )
        # Executes
        #self._Register(
        #    "File.{0}.Executes".format(self.__name),
        #    TesterSet(
        #            testers.RunFile,
        #            self,
        #            self._TestRun.EndEvent,
        #            converter=lambda x: File(self._TestRun, x, runtime=False),
        #            description_group=des_grp
        #        ),"Execute"
        #    )
    
        ## Bind the tests based on values passed in

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
        The absolute path of the file, based on directory relative from the test file location
        '''
        return os.path.normpath(os.path.join(self._TestRun._Test.TestDirectory, self.Name))

    @property
    def Name(self):
        return self.__name

    @Name.setter
    def Name(self, val):
        self.__name = val

    #@property
    #def Exists(self):
    #    return self._GetRegisterEvent("File.{0}.Exists".format(self.__name))

    def GetSize(self):
        statinfo = os.stat(self.AbsPath)
        return statinfo.st_size

    #@property
    #def Size(self):
    #    return self._GetRegisterEvent("File.{0}.Size".format(self.__name))
   
    #@property
    #def Content(self):
    #    return self._GetRegisterEvent("File.{0}.Content".format(self.__name))

    #@Content.setter
    #def Content(self, val):
    #    def getChecker():
    #        des_grp="{0} {1}".format("file",self.Name)
    #        if isinstance(val, testers.Tester):
    #            val.TestValue = self
    #            if value.DescriptionGroup is None:
    #                value.DescriptionGroup=des_grp
    #            return val
    #        elif isinstance(val, str):
    #            return testers.GoldFile(File(self._TestRun, val, runtime=False),
    #                                    test_value=self,description_group=des_grp)
    #        elif isinstance(val, (tuple, list)):
    #            return testers.GoldFileList([File(self._TestRun, item, runtime=False)
    #                                         for item in val], test_value=self,description_group=des_grp)

    #    self._Register("File.{0}.Content".format(self.__name), getChecker,self._TestRun.EndEvent)

    #@property
    #def Executes(self):
    #    return self._GetRegisterEvent("File.{0}.Execute".format(self.__name))

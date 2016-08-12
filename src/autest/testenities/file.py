from __future__ import absolute_import, division, print_function
from autest.common.constructor import call_base, smart_init

from autest.core.testenity import TestEnity
from autest.core.testerset import TesterSet
import autest.testers as testers

import os 

@smart_init
class File(TestEnity):
    '''
    Allows us to test for a file. We can test for size, existance and content
    '''
    @call_base(TestEnity=("runable",))
    def __init__(self, runable, name, exists = None, size = None, content_tester = None,execute=False,runtime=True):
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
                    self._Runable.FinishedEvent,
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
                    self._Runable.FinishedEvent,
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
                    self._Runable.FinishedEvent,
                    converter=lambda x: File(self._Runable, x, runtime=False),
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
        return os.path.normpath(os.path.join(self._RootRunable.RunDirectory, self.Name))

    @property
    def AbsTestPath(self):
        '''
        The absolute path of the file, based on directory relative from the test file location
        '''
        return os.path.normpath(os.path.join(self._RootRunable.TestDirectory, self.Name))

    @property
    def Name(self):
        return self.__name

    @Name.setter
    def Name(self, val):
        self.__name = val

    def GetSize(self):
        statinfo = os.stat(self.AbsPath)
        return statinfo.st_size

   
import autest.core.testrunitem as testrunitem
from .directory import Directory
from .file import File
import hosts.output as host

class Disk(testrunitem.TestRunItem):
    '''
    allows use to define what kind of disk based test we want to do
    '''
    def __init__(self,testrun):
        super(Disk, self).__init__(testrun)
        self.__files={}
        self.__dirs={}

    def File(self, name, exists=None, size=None, content=None, execute=None, id=None,
             runtime=True):
        tmp = File(self._TestRun, name, exists, size, content, execute, runtime)
        if name in self.__files:
            host.WriteWarning("Overriding file object {0}".format(name))
        self.__files[name] = tmp
        if id:
            self.__dict__[id] = tmp
        return tmp

    def Directory(self, name, exists=None, id=None, runtime=True):
        tmp = Directory(self._TestRun, name, exists, runtime)
        if name in self.__dirs:
            host.WriteWarning("Overriding directory object {0}".format(name))
        self.__dirs[name] = tmp
        if id:
            self.__dict__[id] = tmp
        return tmp


import autest.api
autest.api.AddTestRunMember(Disk)
import hosts.output as host
import re

from . import tester
from .file_callback import FileContentCallback
from autest.exceptions.killonfailure import KillOnFailureError

class RegexpContent(FileContentCallback):
    def __init__(self, regexp, description, killOnFailure=False, description_group=None):
        if isinstance(regexp, str):
            regexp = re.compile(regexp)
        self.__regexp = regexp
        FileContentCallback.__init__(self, self.__check, description, killOnFailure,description_group=description_group, description='')
    
    def __check(self, data):
        if not self.__regexp.search(data):
            return 'Contents of {0} do not match desired regexp'.format(self.TestValue.AbsPath)

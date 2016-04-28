import os

import autest.core.setupitem as setupitem
import autest.api as api

class Copy(setupitem.SetupItem):
    def __init__(self,source,target=None):
        super(Copy, self).__init__(
                    itemname="Copy"
                    )
        self.source=source
        self.target=target

    def setup(self):
        self.Copy(self.source,self.target)

class FromDirectory(setupitem.SetupItem):
    def __init__(self,source):
        super(FromDirectory, self).__init__(
                    itemname="Setup test from Directory"
                    )
        self.source=source

    def setup(self):
        self.Copy(self.source,self.SandBoxDir)

class FromTemplate(setupitem.SetupItem):
    def __init__(self,source):
        super(FromTemplate, self).__init__(
                    itemname="Setup test from Template"
                    )
        self.source=source

    def setup(self):
        self.Copy(os.path.join(self.TestRootDir,"templates",self.source),self.SandBoxDir)


api.AddSetupItem(Copy,"__call__",ns='Copy')
api.AddSetupItem(FromDirectory,ns='Copy')
api.AddSetupItem(FromTemplate,ns='Copy')

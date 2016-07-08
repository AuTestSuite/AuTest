import os

import autest.core.setupitem as setupitem
import autest.api as api

class Copy(setupitem.SetupItem):
    def __init__(self,source,target=None,try_link=False):
        super(Copy, self).__init__(
                    itemname="Copy"
                    )
        self.source=source
        self.target=target
        self.try_link=try_link

    def setup(self):
        self.Copy(self.source,self.target,self.try_link)

class FromDirectory(setupitem.SetupItem):
    def __init__(self,source,try_link=False):
        super(FromDirectory, self).__init__(
                    itemname="Setup test from Directory"
                    )
        self.source=source
        self.try_link=try_link

    def setup(self):
        self.Copy(self.source,self.SandBoxDir,self.try_link)

class FromTemplate(setupitem.SetupItem):
    def __init__(self,source,try_link=False):
        super(FromTemplate, self).__init__(
                    itemname="Setup test from Template"
                    )
        self.source=source
        self.try_link=try_link

    def setup(self):
        self.Copy(os.path.join(self.TestRootDir,"templates",self.source),self.SandBoxDir,self.try_link)


api.AddSetupItem(Copy,"__call__",ns='Copy')
api.AddSetupItem(FromDirectory,ns='Copy')
api.AddSetupItem(FromTemplate,ns='Copy')

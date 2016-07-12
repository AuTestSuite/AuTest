import autest.core.setupitem as setupitem
import autest.api as api

class CopyAs(setupitem.SetupItem):
    def __init__(self, source, targetdir, targetname=None):
        super(CopyAs, self).__init__(
            itemname="CopyAs"
        )
        self.source=source
        self.targetdir=targetdir
        self.targetname=targetname

    def setup(self):
        self.CopyAs(self.source, self.targetdir, self.targetname)

api.AddSetupItem(CopyAs,"__call__",ns='CopyAs')
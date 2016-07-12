import autest.core.setupitem as setupitem
import autest.api as api

class MakeDir(setupitem.SetupItem):
    def __init__(self, path):
        super(MakeDir, self).__init__(
            itemname="MakeDir"
        )
        self.path=path

    def setup(self):
        self.MakeDir(self.path)

api.AddSetupItem(MakeDir, "__call__", ns='MakeDir')
import autest.core.setupitem as setupitem
import autest.api as api

class Chown(setupitem.SetupItem):
    def __init__(self, path, uid, gid):
        super(Chown, self).__init__(
            itemname="Chown"
        )
        self.path = path
        self.uid = uid
        self.gid = gid

    def setup(self):
        self.Chown(self.path, self.uid, self.gid)

api.AddSetupItem(Chown,"__call__",ns='Chown')
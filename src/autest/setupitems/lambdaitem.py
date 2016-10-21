from __future__ import absolute_import, division, print_function
import autest.core.setupitem as setupitem
import autest.api as api


class Lambda(setupitem.SetupItem):
    def __init__(self, func, description):
        super(Lambda, self).__init__(itemname="Lamda")
        self.func = func
        self.Description = description

    def setup(self):
        self.func()


api.AddSetupItem(Lambda, "__call__", ns='Lambda')

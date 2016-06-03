from __future__ import absolute_import, division, print_function
import autest.glb as glb
import hosts.output as host


def AddWhenFunction( func,name=None):
    if name is None:
        name = func.__name__

    def wrapper(self,*lst,**kw):
        try:
            return func(*lst,**kw)
        except TypeError:
            return func()

    method = wrapper

    setattr(glb.When,name,method)
    host.WriteVerbose("api",'Added extension function "{0}"'.format(name))
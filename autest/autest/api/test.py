import autest.glb as glb
import hosts.output as host
from autest.core.test import Test
import types

def ExtendTest(func,name=None):
    if name is None:
        name=func.__name__
    method=types.MethodType(func,None,Test)
    setattr(Test,name,method)
    host.WriteVerbose("api",'Added Test extension function "{0}"'.format(name))



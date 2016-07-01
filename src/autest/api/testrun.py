from __future__ import absolute_import, division, print_function
import autest.glb as glb
import hosts.output as host
from autest.core.testrunitem import TestRunItem
from autest.core.testrun import TestRun
import types

def ExtendTestRun( func,name=None,setproperty=False ):
    if name is None:
        name = func.__name__
    
    method = func
    if setproperty:
        method = property(fset=method)

    setattr(TestRun,name,method)
    host.WriteVerbose("api",'Added TestRun extension function "{0}"'.format(name))

def AddTestRunMember( clsobj, name=None, cls=None ):
    # helper function
    #def wrapper( self,*lst,**kw ):
    #        self._add_item(item(*lst,**kw))
    
    if not issubclass(clsobj,TestRunItem):
        host.WriteError("Object must be subclass of autest.core.testrun.testrunitem.TestRunItem")
    
    # get name of task if user did not provide a value
    if name is None:
        name = clsobj.__name__

    if cls is None:
        cls = TestRun

    # get any info that might exist, else return empty dictionary
    cls_info = glb._runtest_items.get(cls,{})
    if name in cls_info:
        host.WriteError("Cannot add user object member {1}.{0}\n {0} already exists on {1} object".format(name, cls.__name__), show_stack=False)
    cls_info[name] = clsobj
    # set the information ( as this might have been the empty dictionary )
    glb._runtest_items[cls] = cls_info


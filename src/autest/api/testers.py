from __future__ import absolute_import, division, print_function
import autest.glb as glb
import hosts.output as host

def AddTester(item, name=None, ns=None):
    # helper function
    def wrapper(self, *lst, **kw):
        self._add_item(item(*lst, **kw))

    # check to make sure this is a SetupItem type
    if not issubclass(item, Tester):
        host.WriteError(
            "Object must be subclass of autest.testers.Tester")

    # get name of task if user did not provide a value
    if name is None:
        name = item.__name__

    if ns is None:
        host.WriteVerbose("setupext",
                          "Adding Tester extension named: {0}".format(name))
        method = wrapper
        setattr(testers, name, method)
    else:
        # see if we have this namespace defined already
        nsobj = glb.setup_items.get(ns)
        if nsobj is None:
            # create the ns object
            nsobj = type(ns, (namespace.NameSpace, ), {})
            # copy on class type as defined for given name
            glb.setup_items[ns] = nsobj
        # add new method to namespace object
        x = wrapper
        setattr(nsobj, name, x)
        host.WriteVerbose(
            "setupext",
            "Adding Tester extension named: {0} to namespace: {1}".format(name,
                                                                         ns))

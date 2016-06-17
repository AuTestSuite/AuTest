from __future__ import absolute_import, division, print_function
import autest.common.process
from autest.common import make_list
import autest.common.is_a as is_a
import hosts.output as host

# need better name...  to do later
class Order(object):
    def __init__( self,*lst,**kw ):
        self.__startbefore = {} # {process : metadata}
        self.__startafter = {}
        self.__endbefore = []
        self.__endafter = []
        super(Order, self).__init__()

    def StartBefore(self, *lst, **kw):
        if lst == () and kw == {}:
            return self.__startbefore
        if lst == () and kw != {}:
            raise SyntaxError

        for obj in lst:
            #validate this is an order object
            if not isinstance(obj, Order):
                host.WriteError("Object must be subclass of autest.core.order.Order")
            readyfunc = kw.get("ready", lambda: obj._isReady())
            args = kw.copy()
            try:
                del args["ready"]
            except KeyError:
                pass
            value = readyfunc
            if is_a.Number(value):
                readyfunc = lambda: obj._hasRunFor(value)
            elif hasattr(readyfunc,"when_wrapper"):
                readyfunc=readyfunc(**args)

            host.WriteDebugf(["startbefore"], "Setting ready logic to wait for process {0} with readyfunc {1}", obj, readyfunc)
            self.__startbefore[obj] = (readyfunc, args)


    def StartAfter(self, *lst, **kw):
        if lst == () and kw == {}:
            return self.__startafter
        if lst == () and kw != {}:
            raise SyntaxError

        for obj in lst:
            #validate this is an order object
            if not isinstance(obj, Order):
                host.WriteError("Object must be subclass of autest.core.order.Order")
            readyfunc = kw.get("ready", lambda: obj._isReady())            
            args = kw.copy()
            try:
                del args["ready"]
            except KeyError:
                pass
            value = readyfunc
            if is_a.Number(value):
                readyfunc = lambda: obj._hasRunFor(value)
            elif hasattr(readyfunc,"when_wrapper"):
                readyfunc=readyfunc(**args)

            host.WriteDebugf(["startafter"], "Setting ready logic to wait for process {0} with readyfunc {1}", obj, readyfunc)
            self.__startafter[obj] = (readyfunc, args)


    def EndBefore(self, *lst, **kw):
        if lst == () and kw == {}:
            return self.__endbefore
        if lst == () and kw != {}:
            raise SyntaxError
        obj = make_list(lst)
        self.__endbefore.extend(obj)

    def EndAfter(self, *lst, **kw):
        if lst == () and kw == {}:
            return self.__endafter
        if lst == () and kw != {}:
            raise SyntaxError
        obj = make_list(lst)
        self.__endafter.extend(obj)



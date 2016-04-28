
import autest.common.process
from autest.common import make_list


# need better name... to do later

class Order(object):
    def __init__(self,*lst,**kw):
        self.__startbefore=[]
        self.__startafter=[]
        self.__endbefore=[]
        self.__endafter=[]
        super(Order, self).__init__()

    @property
    def StartBefore(self):
        return self.__startbefore
    @StartBefore.setter
    def StartBefore(self,obj):
        obj=make_list(obj)
        self.__startbefore.extend(obj)
    @property
    def StartAfter(self):
        return self.__startafter
    @StartAfter.setter
    def StartAfter(self,obj):
        obj=make_list(obj)
        self.__startafter.extend(obj)
    @property
    def EndBefore(self):
        return self.__endbefore
    @EndBefore.setter
    def EndBefore(self,obj):
        obj=make_list(obj)
        self.__endbefore.extend(obj)
    @property
    def EndAfter(self):
        return self.__endafter
    @EndAfter.setter
    def EndAfter(self,obj):
        obj=make_list(obj)
        self.__endafter.extend(obj)




    


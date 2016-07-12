from __future__ import absolute_import, division, print_function
import autest.common.is_a as is_a

# object inherits dict type
class Variables(dict, object): 
    def __init__(self, val=None):
        if val is None:
            val = {}
        if not is_a.Dict(val):
            raise TypeError("value needs to be a dict type") 
        dict.__init__(self)        
        self.update(val)
    
    def __getattr__(self, name):
        try:
            return self[name] 
        except KeyError:
            raise AttributeError("%r has no attribute %r" % 
                                 (self.__class__, name))

    def __setattr__(self, name, value):
        self[name] = value
from __future__ import absolute_import, division, print_function
from builtins import int
from future.utils import native_str 

def List(obj):
    return isinstance(obj,list)

def String(obj):
    return isinstance(obj,native_str)

def Int(obj):
    return isinstance(obj,int)

def Number(obj):
    return isinstance(obj,int) or isinstance(obj,float)

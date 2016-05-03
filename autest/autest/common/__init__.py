
import collections
from . import is_a

def flatten(iterable):
    if isinstance(iterable, collections.Iterable) and not isinstance(iterable,str):
        return [a for i in iterable for a in flatten(i)]
    else:
        return [iterable]

def make_list(obj,flatten_list=True):
    if not is_a.List(obj):
        obj=[obj]
    if flatten_list:
        obj=flatten(obj)
    return obj

# compatable 2 vs 3
def with_metaclass(meta, *bases):
    class metaclass(meta):
        __call__ = type.__call__
        __init__ = type.__init__
        def __new__(cls, name, this_bases, d):
            if this_bases is None:
                return type.__new__(cls, name, (), d)
            return meta(name, bases, d)
    return metaclass('temporary_class', None, {})

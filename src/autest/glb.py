from __future__ import absolute_import, division, print_function

Engine = None

# Object that hold tests functions used
class When(object):
    pass

Locals = {}
# this hold meta information for any items we will add to
# the Setup object
_setup_items = {}
# this hold meta information for any items we will add to
# the runtest objects
_runtest_items = {}

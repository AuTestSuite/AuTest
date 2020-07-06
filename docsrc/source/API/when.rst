When namespace
==============

This namespace contains a set of functions to help with testing when and given process maybe considered ready.
By default without the functions the only valid input is a number which would represent the time in second to wait.
For many application the test to be ready can be defined such as does a file exists on disk.
AuTest contains a various set of functions to help with common items to test for.
More items will be added in future releases.
New items can be added via the extention to add missing logic

Network
-------

These test state of network ports.

.. automodule:: autest.whenitem.portopen
    :members:

File System
-----------

These test state of file or directories on disk.

.. automodule:: autest.whenitem.dirmodified
    :members:

.. automodule:: autest.whenitem.filemodified
    :members:

Random
------

.. automodule:: autest.whenitem.counter
    :members:


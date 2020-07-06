Disk
====

Allows definition of disk entities,
such as Directories and File Objects to be tested as part of the defining scope.
It also store a reference of the object for later access.

.. autoclass:: autest.testenities.disk.Disk()
    :members:
    :inherited-members:

.. note::

    Items that are created can be given an **id** argument which will be used to when making the new
    entity a member of the Disk object.

    **Example**

        .. code::

            Test.Disk.File("foo.txt",id="foo")
            Test.Disk.foo.Exists = True

    Likewise all item can be accessed can be accesses via a read only dictionary interface.
    This allow accessing entities that do not have language friendly names.

    **Example**

        .. code::

            Test.Disk.File("dir/foo.txt")
            Test.Disk["dir/foo.txt"].Exists = True

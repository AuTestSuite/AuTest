Directory
=========

Defines a directory entity on disk that can have a number of checks done on it.

.. autoclass:: autest.testenities.directory.Directory()
    :members:
    :inherited-members:

Testable properties:
--------------------

These are the testable properties of the directory object.

.. py:attribute:: Exists

    Test that the Directory exists or does not exist. If set to None no test will happen

    **Event**
    : Finished

    **Default type**
    : Boolean

    **Example:**

    Test that a directory exists at the end of the Test run

    .. sourcecode:: python

        tr = Test.AddTestRun()
        d = tr.Disk.Directory("logs/plugins")
        d.Exists = True



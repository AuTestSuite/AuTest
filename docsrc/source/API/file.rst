File
====

Defines a file entity on disk that can have a number of checks done on it.
File objects can be extended via subclassing to allow creating new file objects with custom functionality to make dealing with different file types easier to manage and test against.

.. autoclass:: autest.testenities.file.File()
    :members:
    :inherited-members:

Testable properties:
--------------------

These are the testable properties of the file object.

.. py:attribute:: Exists

    Test that the Directory exists or does not exist. If set to None no test will happen

    **Event**
    : Finished

    **Default type**
    : Boolean

    **Example:**

    Test that a file exists at the end of the Test run

    .. sourcecode:: python

        tr = Test.AddTestRun()
        f = tr.Disk.File("logs/errors.log")
        f.Exists = True


.. py:attribute:: Size

    Test that the size is equal the value provided

    **Event**
    : Finished

    **Default type**
    : integer

    **Example**

    Test that a file size is 1024 bytes.

    .. sourcecode:: python

        tr = Test.AddTestRun()
        f = tr.Disk.File("some.data")
        f.Size = 1024

    Test that a file size is less than 1096 bytes.

    .. sourcecode:: python

        tr = Test.AddTestRun()
        f = tr.Disk.File("some.data")
        f.Size = Testers.LessThan(1096)

.. py:attribute:: Content

    Test that the content matches the provided gold file

    **Event**
    : Finished

    **Default type**
    : string ( i.e. file name to gold file)

    **Example:**

    Test that output file matches expected results

    .. sourcecode:: python

        tr = Test.AddTestRun()
        f = tr.Disk.File("out.data")
        f.Content = "gold/content.gold"



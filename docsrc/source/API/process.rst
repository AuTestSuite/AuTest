

Process
=======

Defines a system process that can run as part of the test.

.. autoclass:: autest.testenities.process.Process()
    :members:
    :inherited-members:

.. FIX ME!!
.. py:method:: Streams
    :property:

    An object that defines a number of streams and virtual streams of the process.
    See Streams for more information.

Testable properties:
--------------------

.. py:method:: ReturnCode
    :property:

    Test that the return code equals to the expected value.
    If None, it is expected the process will be killed and will not be able to return a value.

    **Event**
    : Finished

    **Default type**
    : Integer


.. py:method:: Time
    :property:

    Test that the process finished within the time in seconds provided by default.
    This does not kill the process.
    It will only report that after the process finished that it failed meet the requirement of the test.

    **Event**
    : Finished

    **Default type**
    : float


.. py:method:: TimeOut
    :property:

    Stops the process if the process is still running after the time provided in seconds by default.

    **Event**
    : Running

    **Default type**
    : float




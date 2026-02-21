
TestRun
=======

This object define a given step in a test.
It is created via calling the Test.AddTestRun() function.

.. autoclass:: autest.core.testrun.TestRun()
    :members:
    :inherited-members:


Testable properties:
--------------------

.. py:attribute:: StillRunningBefore

    Tests that the process is still running before the test run start running

    **Event**
    : Setup

    **Default type**
    : Process object

    **Example:**

    Test the server process is still running before the second Test Run starts

    .. sourcecode:: python

        p=Test.Processes.Process("ts","myserver –port 8080")
        t1 = Test.AddTestRun("server started properly")
        # ...

        t2 = Test.AddTestRun("server started properly")
        t2.StillRunningBefore=p

.. py:attribute:: StillRunningAfter

    Tests that the process is still running before the test run start running

    **Event**
    : Finished

    **Default type**
    : Process object

    **Example:**

    Test the server process is still running after the test run is command finishes

    .. sourcecode:: python

        p=Test.Processes.Process("ts","myserver –port 8080")
        t1 = Test.AddTestRun("server started properly")
        t1.StillRunningAfter=p
        # ...

.. py:attribute:: NotRunningBefore

    Tests that the process is not running before the test run start running

    **Event**
    : Setup

    **Default type**
    : Process object

.. py:attribute:: NotRunningAfter

    Tests that the process is still running before the test run start running

    **Event**
    : Finished

    **Default type**
    : Process object

    **Example:**

    Test the server process stopped

    .. sourcecode:: python


        P = Test.Processes.Default.Command="myserver –port 8080"
        t = Test.AddTestRun("server started properly")
        t.Processes.Default.Command = "kill-server"
        t.NotRunningAfter = p




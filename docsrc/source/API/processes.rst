Processes
=========

Allows definition of Process objects to run as part of the test.
It also store a reference of the object for later access.

.. autoclass:: autest.testenities.processes.Processes()
    :members:
    :inherited-members:

.. note::

    The name argument is used to define an a name attribute that can be used to access the process later.
    This name should be friendly to values that can be used to define variable in python.

    **Example**

        .. code::

            Test.Processes.Process("server")
            Test.Processes.server.Command = "./myserver --verbose"

    However it does not have to be and in cases in which the value is not safe to access as a member
    a diction like interface exists to access the object.

    **Example**

        .. code::

            Test.Processes.Process("My Server")
            Test.Processes['My Server'].Command = "./myserver --verbose"


General Design
##############

What makes up a test
====================

The basics of defining a test are creating a text file that ends with ".test" or ".test.py".
This file should be added under a root directory that should hold all defined tests.

.. tip::
    Using directories to help organize tests in to related groups to maintaining a large number of tests.

Inside the file the user can define:

* A set of conditions, to control if the test should run or not on the given platform.
* One or more test steps referred to as test runs, that will define one default process to run and a number of items to test various state for.
* Set up actions to copy or do other actions, such as copy files, needed to setup the test to run correctly. The Test and each TestRun and Process defined can have its own setup logic.
* extra File or Directory items that are needed as part of the test to allow testing of content or state.

The name of the test is the file name minus the extension.
The subdirectories can be used to help refer a given test or a set of tests.

A test or verification of state are defined via setting various testable properties of an object to a value or a custom Testable object.
In Autest test will normally continue to run and all failed states will reported at the end.
A given testable property such as `ReturnCode` on a `Process` object have a default tester associated with it
( in this case Equal) that can take a default value (In this case a number).
A give testable property can be given one or more states to test for via using = or += operator or certain composable tester object.
It is important to understand that for the most part, minus local python variable ordering or default creation of TestRun objects, the order in which items are defined in a test file does not matter.
The test file defines context of what needs to happen.
Autest itself will process this and run the items in the correct order.

.. note::
    It is important to understand that the tests are done not done via direct asserts,
    but via setting some state to check for on a property of the Testable object that is normally mapped to some testable property of an object or via an event.
    This is different from many testing systems that are based on running serial code until an assert stop execution of the test.


Objects for Defining Tests
==========================

There are a few objects to allow the defining of tests.
While technically a test file is Python, the design is to maybe allow for different test file formats in the future
because of this to help with ease of use and future compatibility shims that maybe needed,
the objects are inserted into the test files namespace when it is loaded.
This mean you generally only don't need to import python modules into the test file.
The core objects you need should just exist.
You still may want to import other modules to help with custom logic not handled by the provided built-in objects.

Global objects types
--------------------

AuTest defines a few global objects to help define any given test.
A summary of the objects or namespaces that are defined globally are:

**Test**
– This is the main object for defining a test.
The Test object is defined as a singleton as there is only one test per file.
A test consist of one or more steps referred to as TestRun.

**Setup**
– The Setup object allows the user to define logic to run before it starts running the first TestRun.
This logic can be extended by the user to add custom checks that are not builtin to the system.
It is the same object you can access via `Test.Setup`.
There is also a Setup object that is defined as member of the TestRun and Process objects.

**Conditions**
– A namespace with a number of builtin or user define extension functions that can be
called to test for various states to control if some or all of a test should run or be skipped.

**Testers**
– A namespace of the built and user defined objects that can be used to define various test cases.

**When**
– A namespace that defines a number of functions that can be used to tell when a Process is considered ready.
This is used when starting multiple processes for a given TestRun to make sure enough delay happens before starting dependent processes.
For example, a test might be running a curl command through some server.
Using a `When.PortOpen` function would allow the testing system a way to know the server is loaded and listening
allowing autest to know is ok to run the curl command.

Most of these objects or namespaces have a way to extend or add function globally via adding a file under the autest-site directory.
More details can be found under
**Extending AuTest**
section.

Local objects types
-------------------

There are a number of object type that will be used when defining a test.
These object are created via factory functions or are members of existing objects.
Most these object contain various testable properties that can be assigned values to enable testing of some state
Understanding these core object will make it easier to understand how a test is defined.

A summary of the objects that are defined by the system are:

**Disk**
– Is a container and factory object of all disk entities define in the test.
It is a member of the Test, TestRun and Process objects.
Defining a disk entity at one of these level controls when that Entity will be tested.
This also allows a common entity can be defined multiple times in different Disk objects.
This allows as an example, different TestRun object to test different states of a file as a test progresses.
The Disk object itself does not define any testable properties.
New entities defined by a given Disk object become members of the Disk object for later access.

**Directory**
– Defines a directory entity on disk.
These are created by the Disk object.

**Env**
- Defines the environment a Process will run under.
It can be viewed as a Dictionary.
Extensions can add default values.
It is a member of the Test, TestRun and Process objects.
The results of the Environment are composed before a process runs allowing values in define in Process to override value in a TestRun which can override values define in a Test object.

**File**
– Defines a file entity on disk.
File objects can extended to allow the create of different types that have extra properties, testable properties or functionality,
such as writing out data YAML and allowing setting of items in the file as a directory vs a string.
These are created by the Disk object

**Processes**
– Is a container and factory object of all processes we want to run.
It is a member of the Test, and TestRun objects.
The Processes object itself does not define any testable properties.
New process defines by a given Processes object become members of the Processes object for later access.

**Process**
– Defines process entities to run.
Processes can be extended.
These are created Processes object.

**Streams**
– Defines output streams such as stdout.
This object is considered a member of the Process object.

**TestRun**
– Defines a step to run in the test.
Created by the global Test object.
The order in which the TestRun objects are created define the order in which they run in the Test.
TestRun objects can be extended.

**Variables**
- Defines a set variable that can be used to control how tests run.
It can be viewed as a Dictionary, however has the ability to be nested.
Extensions can add default values.
It is a member of the Test, TestRun and Process objects.
The results of the Variables are can be composed allowing values in define in Process to override value in a TestRun which can override values define in a Test object.

How this connects
=================

The general design of the system is based on creating objects that defines events and testable states.
In AuTest these object is referred as a runnable object.
AuTest defines three runnable based objects. These are:

* Test – which defines the test as a whole.
* TestRun – which defines a step of the test.
* Process – which defines a process that is run as part of the test or a given step

The Runnable object defines:

* Common set of events

  #. Setup – called to do any setup logic
  #. Starting – called before we start the main logic of the runnable
  #. Started – called after the main logic has started
  #. Running – is called every .1 of second while the runnable logic is executing
  #. Finished – called after the logic of the runnable has finished
  #. Cleanup – called to do any cleanup actions

* A shell environment of variables to be used to run any processes under it
* Variables object to define custom values to help provide information or control the test logic


Custom logic is added via an extension API to provide common functionality to the different core object used to define tests.
This allows, for example, a Test object to define an API to create custom processes while not allow the TestRun object to have the same API defined.
This provides a level of scope and context of when an object is tested for the state.

.. important::
    The concept of **Scopes** is key to understand when and what gets tested at a given point in time.
    A Scope is any runnable object, which are currently the Test, TestRun and Process objects, that define common set of events.

    For example, a File object defined at a Test scope will have the contents tested when the Test `Finished` event happens.
    Defining a File object at a Process scope will have it the content test happen when the process `Finished` event happens as the test is running.


Running the tests
=================

When running the test program "autest" results in these steps:

#. Load any extensions.
#. Recursively scans a directory for tests to run.
#. For each test found:
    #.   Read the test data.
    #.   Define objects describing the test.
    #.   Setup and Run the test in the sandbox location.
    #.   Collect any result about the test.
#.   Report out the results via the default or user-provided reporter objects.

Various options and features exist to help control the running test.


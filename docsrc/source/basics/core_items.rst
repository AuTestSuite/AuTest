Objects for Defining Tests
==========================

There are a few objects to allow the defining of tests. While technically a test file is Python, the design is to maybe allow for different test file formats in the future, as such, the objects are inserted into the test files namespace when it is loaded. This mean you generally only don't need to import python modules to test file. The core objects you need should just exist. You still may want to import other modules to help with another task not handled by the provided built-in objects, or by the extension loaded by the system. Object are defined globally or require calling some function to create an instance of it.

Global objects
--------------

These objects or namespaces define singleton objects for a test or a group of functions or objects to address a certain need. A summary of the objects or namespaces that are defined globally are:

**Test**
– this is the main object for defining a test. There is only one test per file.
A test consist of one or more steps referred to as TestRun.

**Setup**
– Setup allows the user to define logic for to run before it starts running the first test. It is the same object you can access via Test.Setup.

**Conditions**
– is a namespace with a number of function that can be called to test if a test can run or not

**Testers**
– is a namespace of the test object that can be used to define more complex test cases. For example, a user can define that a return code should be less than 5 vs the default is equal to a value.

**When**
– is a namespace that defines a number of function that can be used to tell when a process is considered ready. This is used when starting multiple processes for a test run and some logic needs to be defined when the next process should be started. For example, a test might be running a curl command through some server. Using a PortOpen function would allow the testing system a way to now when it is ok to run the curl command, giving the server time enough to correct startup.

Most of these objects or namespaces have a way to extend or add function globally via adding a file under the autest-site directory. More details can be found under
**Extending AuTest**
section.

Local objects
-------------

These objects created by calling some function to create an instance of it or they are considered a member of an instance of a created object. These object generally define some testable entities, such as a process, file on disk, or a step of the test to run. Given these are testable there as a number of testable properties defined that can be set to some logic to verify some state. A summary of the objects that are defined by the system are:

**Disk**
– Defines concept of disk entities. Used to create and hold entities in a file system.

**Directory**
– defines a directory entity on disk. These are created by the Disk object

**File**
– Defines a file entity on disk. This can be extended to allow the create of different file types that have extra properties, testable properties or functionality, such as writing out data in a certain format given custom data inputs. These are created by the Disk object

**Processes**
– Defines the set of processes we want to run. Used to create and hold process entities

**Process**
– Defines process entities to run. These are created Processes object.

**Streams**
– Defines output streams such as stdout. This object is considered a member of the Process object.

**TestRun**
– Defines a step to run in the test. Created by the global Test object.


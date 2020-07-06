Introduction
============

The Reusable Gold Testing System (or AuTest for short) is a gold file testing system design to be extensible to allow customization to easily tailor test definition to be more suitable for the given application being tested.
The main goal is to provide a solution to a common testing problem that can be reused and customized.

Vision statement
----------------

The testing system design is based on the idea to be customized.
Most testing systems are very similar to each other and in general, differ on in functionality needed to test a certain domain of applications.
A testing system for a build system might have special functions added to make it easy to test a build run,
while a testing system for a multi-threaded library might have a different set to make it easy to test building and running variable use cases.
In general, the inability to adapt one testing system to test a different application are hard coded design decisions that make it impossible
or very difficult to adapt or use for a different set of applications.
The user can add, or override functionality in the system to adapt it to the needs of the application.
Nothing is perfect, however, this testing system goal is to be reusable, but it is expected that cases exist that may need tweaks or additions to the engine.
Overtime and as more user cases are found the ability to extend and customize should improve.


Goals
----------------------------------

* Easy to write and add tests
* Define an extensible system to allow:

  * Adding new functionality for testing your application
  * Batch commands as a new function to make it easier to write tests
  * Define custom report outputs

* Precise as possible error messages to make it easy to see what is wrong fast
* Sandbox to make it easy to see what failed and reproduce test without of the test system to help with debugging.
* Flexible gold file syntax to make it easier to ignore text that is not important


What is Gold File Testing?
==========================

Gold file testing is classically a process of running one or more applications in a certain order and testing that the console or some other file output matches expected values.
In this testing system, other items that can be tested include:

* Did the process finish?

  * with an expected return code?
  * within a certain time?
  * Is a process still running, or did it crash?

* Did certain files or directories exist or not exist?
* Are the files the right size?
* Does the content of the file or directory contain items we expect to see

Gold testing is a lot like unit testing except that it is done at a process level vs a function API.
In general this style of testing is often used to test:

* Functionality of a process or plugin/extension to another process
* Testing a network application or service
* Test an API or SDK works as expected
* Testing automation pipelines in which a set of actions should result in an expected outcome

There are many other cases in which this style of testing can be a useful way to validate correctness.



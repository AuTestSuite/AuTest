Reusable Gold Testing System
===================================

Reusable Gold testing system, or autest for short, is a testing system targeted toward gold file, command line process testing.

Goals
----------------------------------

* Easy to write and add tests
* Extensible system to allow: 
  * Adding new functionality for testing your application
  * Batch commands as a new function to make it easier to write tests
  * Define custom report outputs
* Precise as possible error messages to make it easy to see what is wrong fast
* Sandbox to make it easy to see what failed and reproduce out of test system
* Flexible gold file syntax to make it easier to ignore text that is not important

Non-Goals
----------------------------------

The Reusable Gold testing system is not about making another unit testing framework.

Requirements
----------------------------------

* Python 3.11 or higher

How do I get set up?
----------------------------------

To install the latest published version:
~~~~
pip install autest
~~~~

To install the latest development version:
~~~~
pip install git+https://github.com/AuTestSuite/AuTest.git
~~~~

For development with uv:
~~~~
uv sync
~~~~

Basic usage
----------------------------------

In the directory containing the tests run:
~~~~
autest
~~~~

Documentation
----------------------------------

Read the [documentation](https://autestsuite.github.io/) to learn how to write and use AuTest in more detail.

Contribution guidelines
----------------------------------

* Feel free to suggest fixes or ask questions
* Have a fix? Submit a pull request!



Tester namespace
================

This namespace provided a number of object predefined testing object to help define a given type of test.
Custom test object can be defined by the user inline of a given test for via the extension API.
It is recommend if a custom test is to be used by for than one test that it should be provided via
the extension API to avoid maintaining issue with keeping multiple copies in sync.

Most testing properties of provide a default tester object that will accept a raw value such as a string or number.
however it common to want to provide a different type of test or a more complex test set.
Using the objects in the tester namespace can make it easy to customize or compose the needed logic

Logical Test
------------

These provide the common equal, less than, etc logic that are needed for basic value testing.

.. autoclass:: autest.testers.equal.Equal

.. autoclass:: autest.testers.not_equal.NotEqual

.. autoclass:: autest.testers.less_than.LessThan

.. autoclass:: autest.testers.less_equal.LessEqual

.. autoclass:: autest.testers.greater_than.GreaterThan

.. autoclass:: autest.testers.greater_equal.GreaterEqual

Content Test
------------

These provide easy way to test the content of a file or text stream.

.. autoclass:: autest.testers.contains_expression.ContainsExpression

.. autoclass:: autest.testers.excludes_expression.ExcludesExpression

.. autoclass:: autest.testers.gold_file.GoldFile

.. autoclass:: autest.testers.zip_content.ZipContent

.. autoclass:: autest.testers.file_callback.FileContentCallback

File System
-----------

Test file system for state.

.. autoclass:: autest.testers.file_exists.FileExists

.. autoclass:: autest.testers.directory_exists.DirectoryExists

Composeable
-----------

Often it is useful to compose a set of test. These objects allow testing for a set of conditions.

.. autoclass:: autest.testers.container.Any

.. autoclass:: autest.testers.container.All

.. autoclass:: autest.testers.container.Not

Lambda
------

When something custom is needed there is a general lambda tester to make it easy to test about anything

.. autoclass:: autest.testers.lambda_tester.Lambda



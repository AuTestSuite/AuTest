Streams
=======

This defines a set of streams and virtual streams that can be tested.
This object is normally a member of process object.
There are a number of virtual stream that are defined to help sort
text in to different groups to help testing related values.
Each virtual stream with match text based on regular expression.
If match if found and the following line start with white space the
that line will be added to test of the virtual stream.
Each stream property if a File object and can be used as such.
By default each property will set a tester object or str to the File.Content testable property.

**Example**

.. code::

    pr.Streams.All = "foo.gold"
    # is the same as
    pr.Streams.All.Content = "foo.gold"
    # location of the all stream data on disk
    pr.Streams.All.AbsPath

Testable properties:
--------------------

.. py:method:: stdout
    :property:

    Tests the output from stdout matches a gold file.

    **Event**
    : Finished

    **Default type**
    : string - file name of the gold file. Path is relative from the location of the test file.

.. py:method:: stderr
    :property:

    Tests the output from stderr matches a gold file.

    **Event**
    : Finished

    **Default type**
    : string - file name of the gold file. Path is relative from the location of the test file.

.. py:method:: All
    :property:

    Tests the mixed output of stdout and stderr matches a gold file.
    Should be what we see on the console.
    However, various buffering behaviors can affect the order seen.

    **Event**
    : Finished

    **Default type**
    : string - file name of the gold file. Path is relative from the location of the test file.

.. py:method:: Debug
    :property:

    A virtual stream that tests the output that is filtered to contain the Debug information.
    The stream will search for a pattern of `'^debug: '` or `'^debug: '`.

    **Event**
    : Finished

    **Default type**
    : string - file name of the gold file. Path is relative from the location of the test file.

.. py:method:: Verbose
    :property:

    Tests the output that is filtered to contain the Verbose information.
    The stream will search for a pattern of `'^verbose: '`.

    **Event**
    : Finished

    **Default type**
    : string - file name of the gold file. Path is relative from the location of the test file.

.. py:method:: Warning
    :property:

    Tests the output that is filtered to contain the Warning information.
    The stream will search for a pattern of `'(\A|\s)warning?\s?(([?!: ])|(\.\s))\D'`.

    **Event**
    : Finished

    **Default type**
    : string - file name of the gold file. Path is relative from the location of the test file.

.. py:method:: Error
    :property:

    Tests the output that is filtered to contain the Error information.
    The stream will search for a pattern of `'(\A|\s)error?\s?(([?!: ])|(\.\s))\D'` or `'fail$'`.

    **Event**
    : Finished

    **Default type**
    : string - file name of the gold file. Path is relative from the location of the test file.


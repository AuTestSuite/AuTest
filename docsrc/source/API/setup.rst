Setup
=====

This general object all defining a set of action to happen in the Setup and Cleanup events.
Use to define actions that need to happen before the object starts.
All actions happen within the sandbox or environment defined for the test.
New methods can be added to main Setup object via the **AddSetupItem** API.
The setup object contains a number of sub-objects that act like domain namespaces to help
separate commonly name actions that might exist in different areas.
For example, different version control tools may have commonly named actions.
These items will be listed below in the form of **<namespace>.<method>** to help clarify grouping.


.. py:method:: FromDirectory(path)

    This method copies items from a given directory to test sandbox directory.
    All paths are relative from the Test.TestRoot directory,
    unless if the path provided is an absolute path.
    The same as:

    .. sourcecode:: python

        Setup.Copy(path, Test.TestRoot)

    Use this function to help provide clarity and intent.

    :arg str path: Path to copy

    **Example**

    Copy all items for directory to be the content of a test.

    .. code:: python

        Setup.Copy.FromDirectory("find_item1")


.. py:method:: Copy.FromTemplate(dir)

    This method copies data from a directory under the template directory under the Test.TestRoot directory.
    The same as:

    .. code:: python

        Setup.Copy(os.path.join(Test.TestRoot,"templates",dir), Test.TestRoot)

    Use this function to help provide clarity and intent.

    :arg str path: Path to copy

    **Example**

    Copies a directory "case1" under the the test root/templates to be the contents of the sandbox

    .. code:: python

        Setup.Copy.FromTemplate("case1")


.. py:method:: Copy(FromPath,ToPath=None)

    This method copies a file or directory to a location under the Sandbox location for the test.
    This is the core function used to by FromTemplate() or FromDirectory().
    The optional ToPath argument can be used to rename the item,
    or to copy the item to a different subdirectory under the sandbox directory.

    :arg str FromPath: Path to copy
    :arg str ToPath: Path to copy

    **Examples**

    Copy a contents of directory to be in the root of the sandbox.
    This is the same as `Setup.FromDirectory("mytestcase")`

    .. code:: python

        Setup.Copy("mytestcase", Test.TestRoot)

    Copy the same directory into the sandbox.
    This create a subdirectory "testit" in the sandbox

    .. code:: python

        Setup.Copy("mytestcase", "testit")

    Copy a file "a.txt" in to the sandbox.

    .. code:: python

        Setup.Copy("a.txt")


.. py:method:: CopyAs(FromPath,ToPath,targetname)

    Will copy the item to the new locations.
    Differs from Copy as the ToPath argument is always viewed as a directory.
    Use this function over the copy function to avoid system behavior hiccup that are common with the use of the OS copy function.

    :arg str FromPath: Path to copy
    :arg str ToPath: Directcory to copy to
    :arg str targetname: name to rename item to under the ToPath

    **Example**

    TBD

.. py:method:: MakeDir(path, mode=None)

    Will create the path provided inside the sandbox.

    :arg str path: The directory to create
    :arg int mode:
        Optional file mode to set the directory to.
        Ignored on systems that don't support this.
        This is system dependent, however on POSIX based system this defaults to 0777 (octal format)


    **Example**

    TBD

.. py:method:: Chown(path, uid, gid, ignore=False)

    Change owner and group is of the item in provided path.

    :arg str path:
        The path to the item to change
    :arg str uid: The user id
    :arg std gid: The group id
    :arg bool ignore: If the value cannot be change, ignore this as an error.


    **Example**

    TBD

.. py:method:: Lambda(func,description)

    A quick and dirty way to do some custom action during setup

    :arg callable func:
        The function to call. Needs to
    :arg description:
        Text to use in the report to describe to the user what the intent step is.

    **Example**

    TBD

.. py:method:: Setup.Svn.CreateRepository(name)

    Create a repository within a directory with the value of "name".

.. py:method:: Setup.Svn.ImportDirectory(name, dir_to_add, sub_dir='')

    Import data to the named SVN repo

    :arg str name:
        The name of the SVN to import to.
        Should be the same value used by CreateRepository()
    :arg str dir_to_add:
        The directory to import into the repository.

    :arg str sub_dir:
        A subdirectory under the repository to import data to, for example, "truck", or "branch"

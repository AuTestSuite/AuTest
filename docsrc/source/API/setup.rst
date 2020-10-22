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


.. py:method:: Copy.FromDirectory(path)

    This method copies items from a given directory to test sandbox directory.
    All paths are relative from the Test.TestRoot directory,
    unless if the path provided is an absolute path.
    The same as saying:

    .. sourcecode:: python

        Setup.Copy(path, Test.TestRoot)

    Use this function to help provide clarity and intent.

    :arg str path: Path to copy

    **Example**

    Copy all items for directory to be the content of a test.

    .. code:: python

        Setup.Copy.FromDirectory("example/case1")


.. py:method:: Copy.FromTemplate(dir)

    This method copies data from a directory under the template directory under the Test.TestRoot directory.
    The same as saying:

    .. code:: python

        Setup.Copy(os.path.join(Test.TestRoot,"templates",dir), Test.TestRoot)

    Use this function to help provide clarity and intent.

    :arg str path: Path to copy

    **Example**

    Copies a directory "case1" under the the test root/templates to be the contents of the sandbox

    .. code:: python

        Setup.Copy.FromTemplate("case1")


.. py:method:: Copy(source, target=None)

    This method copies a file or directory to a location under the Sandbox location for the test.
    This is the core function used to by FromTemplate() or FromDirectory().
    The optional target argument can be used to rename the item,
    or to copy the item to a different subdirectory under the sandbox directory.

    :arg str source: Path to copy
    :arg str target: Path to copy

    **Examples**

    Copy a contents of directory to be in the root of the sandbox.
    Using **Setup.FromDirectory("mytestcase")** may be more clear.

    .. code:: python

        Setup.Copy("mytestcase", Test.TestRoot)

    Copy the same directory into the sandbox.
    This create a subdirectory "testit" in the sandbox

    .. code:: python

        Setup.Copy("mytestcase", "testit")

    Copy a file "a.txt" in to the sandbox.

    .. code:: python

        Setup.Copy("a.txt")


.. py:method:: CopyAs(source, target=None, name)

    Will copy the item to the new locations.
    Differs from Copy as the target argument is always viewed as a directory.
    Use this function over the copy function to avoid system behaviors where that target maybe be viewed as a file or directory depending on if the existence of the target on disk.

    :arg str source: Path to copy
    :arg str target: Directory to copy to. If set to None will be the sandbox directory
    :arg str name: name to rename item to under the ToPath

    **Example**

    This will copy a file to the root sandbox directory

    .. code:: python

        Setup.CopyAs("a.txt")

    This will copy a file to the root sandbox directory and rename the file a1.txt

    .. code:: python

        Setup.CopyAs('a.txt',name='a1.txt')

    This will copy a file to the directory sub1/sub2 and rename the file as a1.txt

    .. code:: python

        Setup.CopyAs("a.txt",'sub1/sub2', 'a1.txt')


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

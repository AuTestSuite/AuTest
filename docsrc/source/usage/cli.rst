Command Line options
####################

AuTest provided a number of command and options to control behavior and functionality.

Commands
********

Command that AuTest supports

run
===

Find and run the tests.
This is the default command that will run is no command is provided

.. program:: autest run

.. option:: --directory <path>
  -D <path>

  The directory to read the tests from.

  *Default:* The current working directory.

  **Examples**:

  .. sourcecode:: shell

      autest -D custom/tests


.. option:: --autest-site <path> [path2 ...]

  A user provided directory for extensions.
  Can be given more than one path. In this case all item will be loaded from both directories in the order of the path values provided.
  If provided the default location will not be used.

  *Default*: to the `autest-site` directory under the path provided by the --directory options, i.e. `./autest-site`

  **Examples**:

  Use a custom path for the extensions

  .. sourcecode:: Bash

    autest -D custom/tests --autest-site ~MyExtensions

  Use more than one path for the extensions.

  .. sourcecode:: Bash

    autest -D custom/tests --autest-site path1 path2

  Can be comma separated

  .. sourcecode:: Bash

    autest -D custom/tests --autest-site path1, path2

  or can be call multiple times

  .. sourcecode:: Bash

    autest -D custom/tests --autest-site path1 --autest-site path2


.. option:: --sandbox path

  The directory in which all the test will run.
  This is useful in cases when the default path may be too long to run a test,
  or when unique locations are desired to keep test results around.
  The directory will be cleared before the run to prevent existing data from corrupting the test run.

  **Defaults** to the value of `./_sandbox`

    Example:

    .. sourcecode:: Bash

        autest --sandbox "run-$(date)"

.. option:: --jobs N
  -j N

  the number of tests to run in parallel.

  **Currently not implemented beyond 1**

  **Defaults** to 1 or running test serially


.. option:: --env var=value [key1=value1]

  Adds a custom variable to the Environment used for running the tests.
  More than one variable can be added.
  Each variable added will replace any existing values in the current shell environment.

  **Examples**:

  .. sourcecode:: Bash

      autest --env PATH=/MyPath:$PATH MYVAR=MyValue


.. option:: --filter <value> [value2 ...]
  -f <value> [value2 ...]

  Filter which tests to run based on the name and location of the test. Wildcard values can pass into help match which test(s) to run.

  **Examples**:

  Run all tests under the basic directory

  .. sourcecode:: Bash

      autest --filter basic/*

  Run all test that end with http

  .. sourcecode:: Bash

      autest --filter http

.. option:: --reporters name [name2 ...]
  -R name [name2, ...]

  Names of optional reporters to run as part of the report generation.
  (Currently there is only the default report generator, more will be added in the future)

.. option:: --clean <level>
  -C <level>

  Level of cleaning for after a test is finished. all >
  exception > failed > warning > passed > skipped >
  unknown> none

  **Defaults** "passed" - which will clean up all passed and skipped tests

  **Examples**:

  Leave no files in the sandbox

  .. sourcecode:: shell

    autest --clean all

  Keep tests that passed. This is useful when creating a new test

  .. sourcecode:: shell

    autest -C passed

  Keep all files in sandbox

  .. sourcecode:: shell

    autest -C none

.. option:: --normalize-kill <value>

  Normalizes the exit code when a process is given SIGKILL to an different value.
  Use this for cases in which the running the tests in an environment (such as certain docker setups)
  in which SIGINIT is blocked and AuTest is forced to kill the process instead.



list
====

List information about test found by the system

.. program:: autest list

.. option:: --json

  output the information in json format

.. option:: --directory <path>
  -D <path>

  The directory to read the tests from.

  *Default:* The current working directory.

.. option:: --filter <value> [value2 ...]
  -f <value> [value2 ...]

  Filter which tests to run based on the name and location of the test. Wildcard values can pass into help match which test(s) to run.

.. option:: --env var=value [key1=value1]

  Adds a custom variable to the Environment used for running the tests.
  More than one variable can be added.
  Each variable added will replace any existing values in the current shell environment.

.. option:: --autest-site <path> [path2 ...]

  A user provided directory for extensions.
  Can be given more than one path. In this case all item will be loaded from both directories in the order of the path values provided.
  If provided the default location will not be used.

  *Default*: to the `autest-site` directory under the path provided by the --directory options, i.e. `./autest-site`


General options
***************

.. program:: autest

.. option:: --version
  -V

  Prints the version of autest being used.

.. option:: --help
  -h

  Print help text

Console options
***************

Options that affect console output

.. option:: --show-color

  show color output <default>

.. option:: --disable-color

  disable color output

.. option:: --verbose [category ...]

  Print extra verbose messages about what the testing system is doing.
  If no argument is provided all messages will be reported.

.. option:: --debug [category ...]

  Print extra information that may help debug what the testing system is doing
  If no argument is provided all messages will be reported.

Release Notes
=============
**Release  1.10.5**

* Add basic setup logic for git repos
* Add documentation for git setup

**Release  1.10.4**

* [Fix] correct logic for stream redirection that resulted for [`PR #29 <https://bitbucket.org/autestsuite/reusable-gold-testing-system/pull-requests/29>`_] that prevented the stream from being redirected correctly

**Release  1.10.3**

* [Fix][`PR #30 <https://bitbucket.org/autestsuite/reusable-gold-testing-system/pull-requests/30>`_] PortOpen: change default address_family to inet
* [Fix][`PR #31 <https://bitbucket.org/autestsuite/reusable-gold-testing-system/pull-requests/31>`_] Add ip6-localhost to PortReady resolution
* updated a verbose message for timeout for a process to become ready when it fails to provide more detail

**Release  1.10.2**

* [Fix][`PR #29 <https://bitbucket.org/autestsuite/reusable-gold-testing-system/pull-requests/29>`_] Improve StreamWriter performance
* [Fix] Exists test for file enities did not work correctly when setting False value in constructor
* Clean up testing logic to include 3.11
* [Fix] Change to using inspect.getfullargspec() api as older API has been removed from python core 

**Release  1.10.1**

* [Fix][`PR #28 <https://bitbucket.org/autestsuite/reusable-gold-testing-system/pull-requests/28>`_] Move collections -> collections.abc for linux cases for 3.10
* [Fix] Use sys.exit() instead of exit()
* Clean up testing logic to include 3.10 and pyston

**Release  1.10.0**

* [Feature][`PR #26 <https://bitbucket.org/autestsuite/reusable-gold-testing-system/pull-requests/26>`_] Allows users to do a case-insensitive compare for their gold files by passing case_insensitive=True to Testers.GoldFile.

**Release  1.9.2**

* [Fix] regression in last release with handling conditions callback as strings or byte strings
* [Fix] Some verbose message that did not format correctly
* Add some tests to address failures founds

**Release  1.9.1**

* [Fix][`PR #24 <https://bitbucket.org/autestsuite/reusable-gold-testing-system/pull-requests/24>`_] Adds tests for CheckOutput handling the --env values
    * Fixes regression found in previous drop that could cause a crash with CheckOutput.

**Release  1.9.0**

* [Fix][`PR #23 <https://bitbucket.org/autestsuite/reusable-gold-testing-system/pull-requests/23>`_] Update documentation for Setup.Copy functions. 
    * Add error message for Setup.CopyAs() when source is a directory
    * Allow target directory for SetupCopyAs to be optional
* [Fix][`PR #22 <https://bitbucket.org/autestsuite/reusable-gold-testing-system/pull-requests/22>`_] Issue with condition and Setup.RunCommand from not processing **--env** argument values correctly
* [Fix][`PR #20 <https://bitbucket.org/autestsuite/reusable-gold-testing-system/pull-requests/20>`_] When.DirExists When.DirNotExists and When.DirModified functions not being imported as expected.

**Release  1.8.1**

* fix regression in tester code.
* update setup.py to fix correct homepage url for site on pypi
* some code clean up

**Release 1.8.0**

* Add in start of redo of documentation with sphinx
* Add timeout logic to TestRun and Test objects
* Fix issues with Variable not accessing values from Parents as expected
* Fix issue with Clean up event not being called
* Fixed issue with running event not being called in certain cases
* updated testing harness to use Nox instead of Tox
* some spelling in fixes in some messages
* fix symlink creation code on windows to better support updates to win32 API for developer mode
* fix to address issue with default process from printing state twice in reports
Release Notes
=============

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
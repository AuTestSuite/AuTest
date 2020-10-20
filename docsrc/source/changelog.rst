Release Notes
=============


**Release  1.8.1**

* [Fix][`PR #20 <https://bitbucket.org/autestsuite/reusable-gold-testing-system/pull-requests/20>`_] When.DirExists When.DirNotExists and When.DirModified functions not being imported as expected.
* [Fix] Issue with condition and Setup.RunCommand from not processing `--env` values correctly

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
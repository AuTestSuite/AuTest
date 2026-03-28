Writting Extensions
===================

One the key features of the AuTest system is the ability to extend the system with different abilities.
This allow making test for a given application look and feel more natural.
For example testing a proxy server may require setting up an origin server and various network call for many of the tests.
While a threading library may need the ability to test that API compiles and run in expected ways.
The goal extending AuTest is to allow the ability to customize the system to make test more desirable
to write and run for the different applications and domains.

At this time the system allow extending of..

* Global helper methods and namespaces loaded from ``autest-site``.
* Testers, setup items, conditions, and runnable-object helpers.
* Custom test formats via ``RegisterTestFormat(...)`` for non-Python test files.

Custom test formats are discovered by filename suffix. For example, an
extension can register ``.test.yaml`` and provide a loader callback that
populates the ``Test`` object directly. These custom formats are available to
both ``autest run`` and ``autest list``.

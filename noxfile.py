import nox


@nox.session(python=["3.11", "3.12", "3.13", "3.14", "3.15"], name="passing")
def passing_tests(session):
    '''Validate tests that should pass'''
    session.install("-e", ".")
    session.run("autest", "-D", "tests/passing")


@nox.session(python=["3.11", "3.12", "3.13", "3.14", "3.15"], name="failing")
def failing_tests(session):
    '''Validate tests that should fail'''
    session.install("-e", ".")
    session.run("autest", "-D", "tests/failing", success_codes=[10])


@nox.session(python=["3.11", "3.12", "3.13", "3.14", "3.15"], name="site")
def site_passing_tests(session):
    '''Validate autest-site test cases'''
    session.install("-e", ".")
    session.run("autest", "-Dtests/site-tests", "--autest-site", "tests/autest-site", "tests/autest-site2")

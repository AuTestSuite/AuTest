import os

Test.Summary = "Tests for superuser privilege"

Test.SkipUnless(Condition.IsElevated("Must have elevated privileges"))

t = Test.AddTestRun("This Test should run")

if os.name == 'nt':
    t.Command = "openfiles"
elif os.name == 'posix':
    t.Command = "sudo -n echo yay we are elevated!"
else:
    Test.SkipIf(Condition.true("Don't know what OS this is. Can't decide on an action to do."))

t.ReturnCode = 0

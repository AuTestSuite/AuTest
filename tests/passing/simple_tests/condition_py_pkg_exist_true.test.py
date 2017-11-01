Test.Summary = "Test that autest exists"

Test.SkipUnless(
    Condition.HasPythonPackage(
        "autest",
        "Package autest doesn't exist? You shouldn't see this."
    ),
)

t = Test.AddTestRun("This Test should run")
t.Command = 'echo "This Test should\'ve run"'
t.ReturnCode = 0

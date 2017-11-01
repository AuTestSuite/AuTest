Test.Summary = "Test that thispackageshouldnotexist doesn't exist in pip"

Test.SkipUnless(
    Condition.HasPythonPackage(
        "thispackageshouldnotexist",
        "Package thispackageshouldnotexist doesn't exist. Good."
    ),
)

t = Test.AddTestRun("This Test should not run")
t.Command = 'echo "This Test should not have run'
t.ReturnCode = 0

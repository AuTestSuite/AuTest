Test.Summary = "Test that max version is to small and we fail"

def out_test(output):
    if "foo" in output:
        return True

Test.SkipUnless(
    Condition.EnsureVersion(
        ["python", "--version"],
        min_version=None,
        max_version="1.1.1"
    ),
)

t = Test.AddTestRun("This Test should not run")
t.Command = 'echo "This Test should not have run"'
t.ReturnCode = 7

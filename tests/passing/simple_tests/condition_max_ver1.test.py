Test.Summary = "Test that we run because the max version is large enough"


def out_test(output):
    if "python" in output.lower():
        return True


Test.SkipUnless(
    Condition.EnsureVersion(
        ["python", "--version"],
        min_version=None,
        max_version="20000.7.0"
    ),
)

t = Test.AddTestRun("This Test should run")
t.Command = 'echo "This Test should have run"'
t.ReturnCode = 0

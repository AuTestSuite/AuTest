Test.Summary = "Test we have a min version to run this test"


def out_test(output):
    if "python" in output.lower():
        return True


Test.SkipUnless(
    Condition.EnsureVersion(
        ["python", "--version"],
        "2.7.0"
    ),
)

t = Test.AddTestRun("This Test should run")
t.Command = 'echo "This Test should have run"'
t.ReturnCode = 0

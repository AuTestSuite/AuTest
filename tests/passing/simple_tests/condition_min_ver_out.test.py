Test.Summary = "Test that min version fails"


def out_test(output):
    if "foo" in output:
        return True


Test.SkipUnless(
    Condition.EnsureVersion(
        ["python", "--version"],
        "100.1000.1000"
    ),
)

t = Test.AddTestRun("This Test should not run")
t.Command = 'echo "This Test should not have run"'
t.ReturnCode = 7

Test.Summary = "Test a condition that should fail because the check function failed"


def out_test(output):
    if "foo" in output:
        return True


Test.SkipUnless(
    Condition.CheckOutput(
        ["python", "--version"],
        out_test,
        "This test should not run because test should fail."
    ),
)

t = Test.AddTestRun("This Test should not run")
t.Command = 'echo "This Test should not have run"'
t.ReturnCode = 7

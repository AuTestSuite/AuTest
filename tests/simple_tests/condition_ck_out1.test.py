Test.Summary = "Test a condition that should pass because the check function should pass"


def out_test(output):
    if "python" in output.lower():
        return True


Test.SkipUnless(
    Condition.CheckOutput(
        ["python", "--version"],
        out_test,
        "This test should always run because this program should exist."
    ),
)

t = Test.AddTestRun("This Test should run")
t.Command = 'echo "This Test should have run"'
t.ReturnCode = 0

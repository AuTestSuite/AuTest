Test.Summary = "Test we fail to run this test because of an invalid args"

def out_test(output):
    if "python" in output.lower():
        return True

Test.SkipUnless(
    Condition.EnsureVersion(
        ["python", "--version"]
    ),
)

t = Test.AddTestRun("This Test should not run")
t.Command = 'echo "This Test should not have run"'
t.ReturnCode = 3

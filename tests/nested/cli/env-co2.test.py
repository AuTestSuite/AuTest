Test.Summary = "Test that --env values are passed to callback function"


# Callback function to check env
def env_test(output):
    if 'testvalue A:B:c' in output:
        return True


# Test env with CheckOutput
Test.SkipUnless(Condition.CheckOutput('echo $MYVALUE $MYLISTVALUE', env_test, "This Test should have run", shell=True))

# test that the shell command works as expected
t = Test.AddTestRun("This Test should run")
t.Command = 'echo "This Test should have run"'
t.ReturnCode = 0

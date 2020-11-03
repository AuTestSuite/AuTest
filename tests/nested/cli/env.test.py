Test.Summary = "Test that --env values are passed to different items that run shell commands"

# note the test is call my a different autest that set the environment with two value
# MYVALUE = testvalue This is set via the --env
# and
# MYLISTVALUE = A:B  This is set value as --env as $MYLISTVALUE:C


def env_test(env):
    if "testvalue" in env:
        return True


Test.SkipIf(Condition.RunCommand('echo $MYVALUE $MYLISTVALUE> condition.txt', "a", "b", shell=True))
Test.Disk.File("condition.txt", content='gold/env-cli.gold')

# test that the Setup works as expected
Setup.RunCommand('echo $MYVALUE $MYLISTVALUE> setup.txt')
Test.Disk.File("setup.txt", content='gold/env-cli.gold')

# test that the shell command works as expected
t = Test.AddTestRun("Testing child")
t.Processes.Default.Command = 'echo $MYVALUE $MYLISTVALUE'
t.Processes.Default.Streams.All = "gold/env-cli.gold"
t.ReturnCode = 0

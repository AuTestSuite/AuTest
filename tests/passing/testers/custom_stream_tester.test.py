Test.Summary = "This is a custom test based on values in the steams"

t = Test.AddTestRun("Get data of Python version")
t.Processes.Default.Command = "python --version"
t.ReturnCode = 0

path = t.Processes.Default.Streams.All.AbsPath


def custom_test(event, tester):
    with open(path) as f:
        data1 = f.read()
    with open(tester.GetContent(event)) as f:
        data2 = f.read()
    if data1 == data2:
        return (True, "Check that versions match", "Python versions did matched")
    else:
        return (False, "Check that versions match", "Python versions did not matched")


t = Test.AddTestRun("Do it again")
t.Processes.Default.Command = "python --version"
t.ReturnCode = 0
t.Processes.Default.Streams.All.Content = Testers.Lambda(custom_test)

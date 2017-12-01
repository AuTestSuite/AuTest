

t = Test.AddTestRun()
t.Processes.Default.Command = 'echo "{}"'.format(Test.Variables.Value)
t.Processes.Default.ReturnCode = 0
t.Processes.Default.Streams.stdout = Testers.ContainsExpression(
    "autest-site2",
    "Load order is incorrect"
)

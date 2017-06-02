test.Summary="Test the setup of Setup Copy logic"

Setup.RunCommand('true')
Setup.RunCommand('true', 0)
Setup.RunCommand('false', 1)

t=Test.AddTestRun("This Test should run")
t.Command='echo "This Test should have run"'
t.ReturnCode=0

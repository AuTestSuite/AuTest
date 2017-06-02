test.Summary="Test the setup of Setup Copy logic"

Setup.RunCommand('false')
Setup.RunCommand('true', 1)
Setup.RunCommand('false', 0)

t=Test.AddTestRun("This Test should not run")
t.Command='echo "This Test should not have run"'
t.ReturnCode=5

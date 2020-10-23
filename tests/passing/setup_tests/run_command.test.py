test.Summary = "Test the setup of Setup Copy logic"

Setup.RunCommand('python -c "import sys; sys.exit(0)"')
Setup.RunCommand('python -c "import sys; sys.exit(0)"', 0)
Setup.RunCommand('python -c "import sys; sys.exit(1)"', 1)

t = Test.AddTestRun("This Test should run")
t.Command = 'echo "This Test should have run"'
t.ReturnCode = 0

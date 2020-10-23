
Test.Summary = "Test a case of is ready logic for start different propocesses"

Setup.Copy("app.py")

tr = Test.AddTestRun()
tr.Processes.Default.Command = "python app.py 1 --ret 5"
tr.Processes.Default.ReturnCode = Not(0)
tr.Processes.Default.ReturnCode += 5

tr = Test.AddTestRun()
tr.Processes.Default.Command = "python app.py 1 --ret 5"
tr.Processes.Default.ReturnCode += 5

tr = Test.AddTestRun()
tr.Processes.Default.Command = "python app.py 1 --ret 5"
tr.Processes.Default.ReturnCode = [5]

tr = Test.AddTestRun()
tr.Processes.Default.Command = "python app.py 1 --ret 5"
tr.Processes.Default.ReturnCode = All(5, Testers.NotEqual(0))

tr = Test.AddTestRun()
tr.Processes.Default.Command = "python app.py 1 --ret 5"
tr.Processes.Default.ReturnCode = All(5, Not(Testers.Equal(0)))

tr = Test.AddTestRun()
tr.Processes.Default.Command = "python app.py 1 --ret 5"
tr.Processes.Default.ReturnCode = All(5, Not(0))

tr = Test.AddTestRun()
tr.Processes.Default.Command = "python app.py 1 --ret 5"
tr.Processes.Default.ReturnCode = Any(5, 0)

tr = Test.AddTestRun()
tr.Processes.Default.Command = "python app.py 1 --ret 5"
tr.Processes.Default.ReturnCode = Any(5, 0)

tr = Test.AddTestRun()
tr.Processes.Default.Command = "python app.py 1 --ret 5"
tr.Processes.Default.ReturnCode = All(5, Not(0))

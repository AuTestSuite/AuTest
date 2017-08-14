Test.Summary = "Test the we will not fail when a timeout is set"

Setup.Copy("server.py", "server")

tr = Test.AddTestRun()
tr.Command = "python server --time=10"
tr.TimeOut = Not(Testers.LessThan(1, "TotalRunTime", kill_on_failure=True))


Test.Summary = "Test the we fail when a timeout is set at the TestRun level"

Setup.Copy("server.py", "server")

tr = Test.AddTestRun()
tr.TimeOut = 1
tr.Command = "python server --time=10"
# given we have no default timeout for a process...
# we remove this possible event to clarify we only test for the timeout at the expected level
tr.Processes.Default.TimeOut.Clear()
# should never run
tr.ReturnCode = 0

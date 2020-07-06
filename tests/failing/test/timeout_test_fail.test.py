Test.Summary = "Test the we fail when a timeout is set at the Test level"

Setup.Copy("server.py", "server")

Test.TimeOut = 1

tr = Test.AddTestRun()
tr.Command = "python server --time=10"
# given we have no default timeout for a process...
# we remove this possible event to clarify we only test for the timeout at the expected level
tr.Processes.Default.TimeOut.Clear()
# should never run
tr.ReturnCode = 0
